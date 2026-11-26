"""Точка входа в приложение."""

import flet as ft

from src.core.config import settings
from src.ui.app_shell import AppShell


async def main(page: ft.Page):
    page.title = settings.app_title
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW

    shell = AppShell(page, app_title=settings.app_title)
    page.add(shell)


if __name__ == "__main__":
    ft.run(main)