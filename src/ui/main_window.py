"""Главное окно приложения."""

import flet as ft


class MainWindow(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.expand = True
        self.spacing = 16
        self.scroll = ft.ScrollMode.AUTO

        # Заголовок или статусная строка экрана
        self.header = ft.Text(
            value="Панель управления",
            size=24,
            weight=ft.FontWeight.BOLD,
        )

        # Контейнер, куда мы будем добавлять ваши кнопки и переключатели
        self.controls_area = ft.Column(spacing=12)

        # Собираем элементы главного окна
        self.controls = [
            self.header,
            ft.Divider(),
            self.controls_area,
        ]
