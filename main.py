"""Точка входа в приложение."""

import flet as ft
from src.core.config import settings
from ui.main_window import MainWindow


async def main(page: ft.Page):
    # Глобальные настройки страницы
    page.title = settings.app_title
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20

    # Верхняя панель приложения (AppBar)
    page.appbar = ft.AppBar(
        title=ft.Text(settings.app_title),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )

    # Инициализируем и добавляем главное окно
    main_window = MainWindow(page)
    page.add(main_window)


if __name__ == "__main__":
    ft.run(main)
