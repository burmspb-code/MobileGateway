"""Главное окно приложения."""

import asyncio
import flet as ft


class MainWindow(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.expand = True
        self.spacing = 16
        self.scroll = ft.ScrollMode.AUTO
        self.is_running: bool = False
        self.seconds: int = 0

        # Заголовок или статусная строка экрана
        self.header = ft.Text(
            value="Панель управления",
            size=24,
            weight=ft.FontWeight.BOLD,
        )

        # Текст для отображения времени таймера
        self.timer_text = ft.Text(
            value="00:00",
            size=48,
            weight=ft.FontWeight.BOLD,
        )

        # Добавляем кнопки
        self.start_btn = ft.FilledButton(
            content="Запустить",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.on_start_click,
        )

        self.stop_btn = ft.OutlinedButton(
            content="Остановить",
            icon=ft.Icons.STOP,
            on_click=self.on_stop_click,
        )

        # Контейнер, куда мы будем добавлять ваши кнопки и переключатели
        self.controls_area = ft.Column(
            spacing=16,
            controls=[
                self.timer_text,
                ft.Row(
                    spacing=12,
                    controls=[self.start_btn, self.stop_btn],
                )
            ],
        )

        # Собираем элементы главного окна
        self.controls = [
            self.header,
            ft.Divider(),
            self.controls_area,
        ]

    def _format_time(self) -> str:
        """Переводит секунды в формат ММ:СС."""
        minutes, secs = divmod(self.seconds, 60)
        return f"{minutes:02d}:{secs:02d}"

    async def _timer_loop(self):
        """Асинхронный цикл, который тикает каждую секунду."""
        while self.is_running:
            await asyncio.sleep(1)
            # Проверяем флаг ещё раз после сна на случай, если кнопку нажали во время ожидания
            if not self.is_running:
                break
            self.seconds += 1
            self.timer_text.value = self._format_time()
            self.update()

    def on_start_click(self, e: ft.ControlEvent):
        if self.is_running:
            return

        self.is_running = True
        self.header.value = "Статус: Таймер запущен"
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.update()

        # Запускаем асинхронную задачу в фоне через Flet
        self._page.run_task(self._timer_loop)

    def on_stop_click(self, e: ft.ControlEvent):
        self.is_running = False
        self.header.value = "Статус: Пауза"
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.update()