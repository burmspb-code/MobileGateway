"""Экран настроек подключения (заглушка, без сохранения и HTTP)."""

import flet as ft


class SettingsView(ft.Column):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.spacing = 16
        self.scroll = ft.ScrollMode.AUTO
        # Растягиваем карточки на всю ширину экрана
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        self.api_url = ft.TextField(
            label="Адрес сервера",
            hint_text="http://192.168.1.100:8000",
            keyboard_type=ft.KeyboardType.URL,
            border_radius=10,
        )
        self.api_token = ft.TextField(
            label="Токен",
            password=True,
            can_reveal_password=True,
            border_radius=10,
        )
        self.health_endpoint = ft.TextField(
            label="Endpoint проверки",
            value="/health",
            border_radius=10,
            expand=2,
        )
        self.timeout = ft.TextField(
            label="Таймаут, сек",
            value="10",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_radius=10,
            expand=1,
        )

        # Карточка с полями ввода
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
                        # Ставим endpoint и таймаут в один ряд, чтобы сэкономить место
                        ft.Row(
                            spacing=12,
                            controls=[
                                self.health_endpoint,
                                self.timeout,
                            ],
                        ),
                        ft.FilledButton(
                            "Сохранить",
                            icon=ft.Icons.SAVE,
                            on_click=self._save_stub,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.Padding.symmetric(vertical=14),
                            ),
                        ),
                        ft.OutlinedButton(
                            "Проверить соединение",
                            icon=ft.Icons.WIFI_FIND,
                            on_click=self._check_stub,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                padding=ft.Padding.symmetric(vertical=14),
                            ),
                        ),
                    ],
                ),
            ),
        )

        self.result_text = ft.Text(
            "Проверка соединения ещё не выполнялась.",
            size=14,
            color=ft.Colors.ON_SURFACE_VARIANT,
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

        self.controls = [
            form_card,
            self.result_card,
        ]

    def _save_stub(self, e):
        self.result_text.value = "Сохранение пока не подключено (заглушка)."
        self.result_text.color = ft.Colors.ON_SURFACE
        self.update()

    def _check_stub(self, e):
        self.result_text.value = "Проверка соединения пока не подключена (заглушка)."
        self.result_text.color = ft.Colors.ON_SURFACE
        self.update()
