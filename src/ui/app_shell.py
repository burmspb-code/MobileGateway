"""Каркас приложения: основная навигация и служебный экран настроек."""

import flet as ft

from src.core.api_client import ApiClient
from src.core.config import ConnectionSettings
from src.core.settings_store import SettingsStore
from src.ui.views.home_view import HomeView
from src.ui.views.settings_view import SettingsView


class AppShell(ft.Column):
    def __init__(
        self,
        page: ft.Page,
        app_title: str = "Mobile Gateway",
        settings_store: SettingsStore | None = None,
        api_client: ApiClient | None = None,
    ):
        super().__init__()
        self._page = page
        self.app_title = app_title
        self.settings_store = settings_store
        self.api_client = api_client
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.STRETCH

        self.current_primary = "home"
        self.current_view = "home"
        self.connection_settings = self.settings_store.load() if self.settings_store else ConnectionSettings()

        self.home_view = HomeView(on_open_settings=self.open_settings)
        self.settings_view = SettingsView(
            initial=self.connection_settings,
            on_save=self._on_settings_saved,
            on_check=self._on_check_connection,
        )

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
            content=self.home_view,
        )
        self.controls = [self.content_host]

        self._sync_home_summary()

    def open_settings(self):
        self.current_view = "settings"
        self._render()

    def _go_back(self, e):
        self.current_view = self.current_primary
        self._render()

    def _on_settings_saved(self, settings: ConnectionSettings):
        self.connection_settings = settings
        if self.settings_store:
            self.settings_store.save(settings)
        self._sync_home_summary()

    async def _on_check_connection(self, settings: ConnectionSettings):
        if self.api_client is None:
            from src.core.api_client import HealthCheckResult
            return HealthCheckResult(False, None, "Клиент API не настроен.")

        result = await self.api_client.check_health(settings)
        if result.ok:
            self.home_view.set_connection_summary(
                status="Подключено",
                details=f"Адрес: {settings.api_url}\n{result.message}",
                is_configured=True,
            )
        else:
            self.home_view.set_connection_summary(
                status="Ошибка подключения",
                details=f"Адрес: {settings.api_url}\n{result.message}",
                is_configured=bool(settings.api_url),
            )
        return result

    def _sync_home_summary(self):
        settings = self.connection_settings
        if settings.api_url:
            self.home_view.set_connection_summary(
                status="Сохранено",
                details=f"Адрес: {settings.api_url}\nEndpoint: {settings.health_endpoint}",
                is_configured=True,
            )
        else:
            self.home_view.set_connection_summary(
                status="Не настроено",
                details="Адрес сервера не задан. Откройте настройки для подключения.",
                is_configured=False,
            )

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