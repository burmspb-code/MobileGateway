"""Главный рабочий экран (заглушка под будущие серверные действия)."""

import flet as ft


class HomeView(ft.Column):
    def __init__(self, on_open_settings):
        super().__init__()
        self.on_open_settings = on_open_settings
        self.expand = True
        self.spacing = 16
        self.scroll = ft.ScrollMode.AUTO
        # Растягиваем все карточки на всю ширину экрана
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        self.connection_status = ft.Text(
            "Не настроено",
            size=12,
            weight=ft.FontWeight.W_600,
            color=ft.Colors.ON_SECONDARY_CONTAINER,
        )
        self.status_badge = ft.Container(
            content=self.connection_status,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            padding=ft.Padding.symmetric(horizontal=10, vertical=4),
            border_radius=12,
        )

        self.connection_details = ft.Text(
            "Адрес сервера не задан. Откройте настройки для подключения.",
            size=14,
            color=ft.Colors.ON_SURFACE_VARIANT,
        )

        self.actions_card = ft.Card(
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
                        ft.Text("Действия сервера", size=18, weight=ft.FontWeight.W_600),
                        ft.Text(
                            "Здесь появятся команды сервера на следующих шагах.",
                            size=14,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                ),
            ),
        )

        self.controls = [
            ft.Card(
                elevation=0,
                bgcolor=ft.Colors.SURFACE,
                shape=ft.RoundedRectangleBorder(
                    radius=16,
                    side=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
                ),
                content=ft.Container(
                    padding=16,
                    content=ft.Column(
                        spacing=12,
                        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text(
                                        "Подключение к серверу",
                                        size=18,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    self.status_badge,
                                ],
                            ),
                            self.connection_details,
                            ft.FilledButton(
                                "Открыть настройки",
                                icon=ft.Icons.SETTINGS,
                                on_click=self._open_settings,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    padding=ft.Padding.symmetric(vertical=14),
                                ),
                            ),
                        ],
                    ),
                ),
            ),
            self.actions_card,
        ]

    def _open_settings(self, e):
        self.on_open_settings()

    def set_connection_summary(self, status: str, details: str, is_configured: bool = False):
        """Обновляет статус подключения и показывает блок действий при готовности."""
        self.connection_status.value = status
        self.connection_details.value = details

        # Меняем цвет бейджа и показываем блок действий, когда сервер настроен
        if is_configured:
            self.status_badge.bgcolor = ft.Colors.PRIMARY_CONTAINER
            self.connection_status.color = ft.Colors.ON_PRIMARY_CONTAINER
            self.actions_card.visible = True
        else:
            self.status_badge.bgcolor = ft.Colors.SECONDARY_CONTAINER
            self.connection_status.color = ft.Colors.ON_SECONDARY_CONTAINER
            self.actions_card.visible = False

        try:
            self.update()
        except RuntimeError:
            # Контрол ещё не добавлен на страницу (например, при инициализации shell).
            pass
