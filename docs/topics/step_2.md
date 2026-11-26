---
title: Реализация шага №2
status: active
created: 2026-11-25
---

## Цель
Реализовать по `docs/step_2.md` экран настроек подключения, локальное сохранение параметров и проверку связи с сервером, не ломая тестовые Start/Stop.

## Решено
- Шаг 2 выделен в отдельную тему; темы «Старт» и «Разработка GUI» закрыты 2026-11-25.
- Тестовый таймер/Start-Stop убран: он был нужен только для проверки UI, Главная теперь рабочая заглушка под будущие действия сервера.
- Настройки — служебный экран, открывается через `⚙` в AppBar; архитектура UI разделена на `AppShell` + отдельные view.
- Настройки хранить через `SettingsStore`: `page.client_storage`, при недоступности — fallback в `connection_settings.json` (файл в `.gitignore`). Токен не логировать и не показывать в ошибках UI.
- Проверку связи делать конфигурируемой: `API_URL` + `HEALTH_ENDPOINT` через `httpx`. Ручная проверка на реальном VPS endpoint `https://194.58.223.7:8443/health` вернула `200`.

## Сделано
- Создана карточка темы, добавлена строка в `docs/topics/INDEX.md`.
- Собран каркас UI: `AppShell`, `HomeView`, `SettingsView`; таймер/Start-Stop удалены, настройки открываются через `⚙`.
- Добавлена модель `ConnectionSettings` с нормализацией/валидацией (`api_url`, `api_token`, `health_endpoint`, `timeout`).
- Добавлен `SettingsStore` (сохранение/загрузка настроек, fallback JSON).
- Добавлен `ApiClient` для async-проверки `GET {API_URL}{HEALTH_ENDPOINT}` через `httpx`; результат выводится в UI, токен не логируется.
- Ручная проверка на ПК: ввод/валидация, сохранение между перезапусками, проверка реального endpoint `https://194.58.223.7:8443/health` — `Соединение установлен (200)`.

## Блокировка
Финальный контракт сервера пока не зафиксирован (нужен ли токен постоянно, какие ещё endpoint’ы будут у Start/Stop). Проверка соединения уже работает на тестовом VPS; для закрытия шага 2 нужен smoke-test на Android/APK.

## Следующий шаг
Провести smoke-test на Android (`flet run --android` / APK): ввод настроек, сохранение, проверка соединения, поведение при отсутствии сети. После этого зафиксировать результат в карточке и решить, закрывать ли шаг 2.

## Файлы
- `.gitignore`
- `docs/step_2.md`
- `docs/topics/INDEX.md`
- `docs/handoff.md`
- `main.py`
- `src/core/config.py`
- `src/core/settings_store.py`
- `src/core/api_client.py`
- `src/ui/app_shell.py`
- `src/ui/views/home_view.py`
- `src/ui/views/settings_view.py`
- `tests/` (тесты ещё не добавлены)

## Затронутые темы
- [Старт](closed/start.md) — закрыта 2026-11-25; `main.py`, `src/core/config.py`, `src/ui/main_window.py`, `docs/topics/INDEX.md`, `docs/handoff.md` переданы в эту тему.
- [Разработка GUI](closed/gui.md) — закрыта 2026-11-25; её следующий шаг (шаг 2) перенесён сюда, файлы каркаса пересекаются.

## Связи
- _нет_
