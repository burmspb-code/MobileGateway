"""Каркас приложения: основная навигация и служебный экран настроек."""

import flet as ft

from src.ui.views.home_view import HomeView
from src.ui.views.settings_view import SettingsView


class AppShell(ft.Column):
    def __init__(self, page: ft.Page, app_title: str = "Mobile Gateway"):
        super().__init__()
        self._page = page
        self.app_title = app_title
        self.expand = True

        # Растягиваем содержимое на всю ширину экрана
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        self.current_primary = "home"
        self.current_view = "home"

        self.home_view = HomeView(on_open_settings=self.open_settings)
        self.settings_view = SettingsView()

        self.back_button = ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            tooltip="Назад",
            on_click=self._go_back,
            visible=False,
        )
        self.settings_button = ft.IconButton(
            icon=ft.Icons.SETTINGS,
            tooltip="Настройки",
            on_click=lambda e: self.open_settings(),
        )

        self.title = ft.Text(self.app_title)
        self._page.appbar = ft.AppBar(
            leading=self.back_button,
            title=self.title,
            center_title=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            actions=[self.settings_button],
        )

        self.content_host = ft.Container(
            expand=True,
            padding=16,
            content=self.home_view
        )
        self.controls = [self.content_host]

    def open_settings(self):
        self.current_view = "settings"
        self._render()

    def _go_back(self, e):
        self.current_view = self.current_primary
        self._render()

    def _render(self):
        if self.current_view == "settings":
            self.back_button.visible = True
            self.settings_button.visible = False
            self.title.value = "Настройки"
            self.content_host.content = self.settings_view
        else:
            self.back_button.visible = False
            self.settings_button.visible = True
            self.title.value = self.app_title
            self.content_host.content = self.home_view

        self._page.update()