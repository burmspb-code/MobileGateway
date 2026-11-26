"""Точка входа в приложение."""

import flet as ft

from src.core.api_client import ApiClient
from src.core.config import settings
from src.core.settings_store import SettingsStore
from src.ui.app_shell import AppShell


async def main(page: ft.Page):
    page.title = settings.app_title
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW

    store = SettingsStore(page)
    api_client = ApiClient()
    shell = AppShell(
        page,
        app_title=settings.app_title,
        settings_store=store,
        api_client=api_client,
    )
    page.add(shell)


if __name__ == "__main__":
    ft.run(main)