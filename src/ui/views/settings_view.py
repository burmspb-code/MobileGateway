"""Экран настроек подключения: ввод, валидация, сохранение и проверка."""

import flet as ft

from src.core.config import ConnectionSettings


class SettingsView(ft.Column):
    def __init__(self, initial: ConnectionSettings | None = None, on_save=None, on_check=None):
        super().__init__()
        self.on_save = on_save
        self.on_check = on_check
        self.expand = True
        self.spacing = 16
        self.scroll = ft.ScrollMode.AUTO
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        initial = (initial or ConnectionSettings()).normalized()
        self._saved = initial

        self.api_url = ft.TextField(
            label="Адрес сервера",
            hint_text="http://192.168.1.100:8000",
            value=initial.api_url,
            keyboard_type=ft.KeyboardType.URL,
            border_radius=10,
        )
        self.api_token = ft.TextField(
            label="Токен",
            value=initial.api_token,
            password=True,
            can_reveal_password=True,
            border_radius=10,
        )
        self.health_endpoint = ft.TextField(
            label="Endpoint проверки",
            value=initial.health_endpoint,
            border_radius=10,
            expand=2,
        )
        self.timeout = ft.TextField(
            label="Таймаут, сек",
            value=str(int(initial.timeout)) if initial.timeout.is_integer() else str(initial.timeout),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=1,
        )

        self.result_text = ft.Text(
            "Проверка соединения ещё не выполнялась.",
            size=14,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        self.save_button = ft.FilledButton(
            "Сохранить",
            icon=ft.Icons.SAVE,
            on_click=self._save,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.symmetric(vertical=14),
            ),
        )
        self.check_button = ft.OutlinedButton(
            "Проверить соединение",
            icon=ft.Icons.WIFI_FIND,
            on_click=self._check,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.symmetric(vertical=14),
            ),
        )

        form_card = ft.Card(
            elevation=0,
            bgcolor=ft.Colors.SURFACE,
            shape=ft.RoundedRectangleBorder(
                radius=16,
                side=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            ),
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=14,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    controls=[
                        ft.Text(
                            "Параметры сервера",
                            size=18,
                            weight=ft.FontWeight.W_600,
                        ),
                        self.api_url,
                        self.api_token,
                        ft.Row(
                            spacing=12,
                            controls=[
                                self.health_endpoint,
                                self.timeout,
                            ],
                        ),
                        self.save_button,
                        self.check_button,
                    ],
                ),
            ),
        )

        self.result_card = ft.Card(
            elevation=0,
            bgcolor=ft.Colors.SURFACE,
            shape=ft.RoundedRectangleBorder(
                radius=16,
                side=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            ),
            content=ft.Container(
                padding=16,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text(
                            "Результат проверки",
                            size=16,
                            weight=ft.FontWeight.W_600,
                        ),
                        self.result_text,
                    ],
                ),
            ),
        )

        self.controls = [form_card, self.result_card]

    def has_unsaved_changes(self) -> bool:
        current = ConnectionSettings(
            api_url=self.api_url.value or "",
            api_token=self.api_token.value or "",
            health_endpoint=self.health_endpoint.value or "/health",
            timeout=self._parse_timeout(),
        ).normalized()
        return current != self._saved

    def revert(self):
        self._apply_normalized(self._saved)
        self._show_message("????????? ?? ?????????.", error=False)
        self.update()

    def _parse_timeout(self) -> float:
        timeout_raw = (self.timeout.value or "").strip()
        try:
            return float(timeout_raw)
        except ValueError:
            return self._saved.timeout

    def _read_form(self) -> tuple[ConnectionSettings | None, list[str]]:
        errors: list[str] = []
        timeout_raw = (self.timeout.value or "").strip()
        try:
            timeout = float(timeout_raw)
        except ValueError:
            errors.append("Таймаут должен быть числом.")
            timeout = 10.0

        settings = ConnectionSettings(
            api_url=self.api_url.value or "",
            api_token=self.api_token.value or "",
            health_endpoint=self.health_endpoint.value or "/health",
            timeout=timeout,
        )
        errors.extend(settings.validate())
        if errors:
            return None, errors
        return settings.normalized(), []

    def _show_message(self, message: str, *, error: bool = False):
        self.result_text.value = message
        self.result_text.color = ft.Colors.ERROR if error else ft.Colors.ON_SURFACE
        self.update()

    def _show_errors(self, errors: list[str]):
        self._show_message("Ошибка ввода:\n- " + "\n- ".join(errors), error=True)

    def _apply_normalized(self, settings: ConnectionSettings):
        self.api_url.value = settings.api_url
        self.api_token.value = settings.api_token
        self.health_endpoint.value = settings.health_endpoint
        self.timeout.value = (
            str(int(settings.timeout)) if settings.timeout.is_integer() else str(settings.timeout)
        )

    def save_settings(self) -> bool:
        """Валидирует и сохраняет настройки. Возвращает True при успехе."""
        settings, errors = self._read_form()
        if errors:
            self._show_errors(errors)
            return False

        self._apply_normalized(settings)
        self._saved = settings
        self._show_message("Настройки сохранены.")
        if self.on_save:
            self.on_save(settings)
        return True

    def _save(self, e):
        self.save_settings()

    async def _check(self, e):
        settings, errors = self._read_form()
        if errors:
            self._show_errors(errors)
            return

        self._apply_normalized(settings)
        self.check_button.disabled = True
        self._show_message(f"Проверяем соединение: {settings.health_check_url}")

        try:
            if self.on_check is None:
                self._show_message("Проверка соединения пока не подключена.", error=True)
                return

            result = await self.on_check(settings)
            self._show_message(result.message, error=not result.ok)
        finally:
            self.check_button.disabled = False
            self.update()