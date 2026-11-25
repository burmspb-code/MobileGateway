---
title: Старт
status: closed
created: 2026-11-24
---

## Цель
Подготовить начальный каркас MobileGateway и рабочий процесс ведения тем в репозитории.

## Решено
- Память о задачах ведётся в файлах `docs/topics/`, одна тема — одна сессия.
- Для старта/финиша/смены темы используются фразы-триггеры из `AGENTS.md` и `docs/workflow.md`.

## Сделано
- Добавлен универсальный `AGENTS.md` и документация рабочего процесса (`docs/INDEX.md`, `docs/workflow.md`, `docs/handoff.md`, `docs/decisions.md`, шаблон темы).
- Добавлен базовый каркас приложения: `pyproject.toml`/`poetry.lock`, `main.py`, `src/core/config.py`, `src/core/settings.py`, `src/ui/main_window.py`, пакетные `__init__.py`, `tests/__init__.py`.
- Добавлены `.env.sample`, `README.md`, `ИНСТРУКЦИЯ.md`, `КОМАНДЫ.md`.
- В `docs/INDEX.md` задана команда тестов: `poetry run pytest -q; if ($LASTEXITCODE -eq 5) { exit 0 } exit $LASTEXITCODE` (exit code 5 = нет тестов, не ошибка).
- Тема закрыта 2026-11-25: каркас передан в тему «Разработка GUI», затем — в тему «Реализация шага №2».

## Блокировка
нет

## Следующий шаг
нет (тема закрыта 2026-11-25; уточнение правил проекта в `docs/INDEX.md` остаётся вне шага 2).

## Файлы
- `AGENTS.md`
- `.env.sample`
- `.idea/mobilegateway.iml`
- `.opencode/commands/docs.md`
- `README.md`
- `docs/INDEX.md`
- `docs/decisions.md`
- `docs/handoff.md`
- `docs/workflow.md`
- `docs/topics/INDEX.md`
- `docs/topics/_template.md`
- `docs/topics/closed/INDEX.md`
- `docs/topics/closed/start.md`
- `main.py`
- `poetry.lock`
- `pyproject.toml`
- `src/__init__.py`
- `src/core/__init__.py`
- `src/core/assets/__init__.py`
- `src/core/config.py`
- `src/core/settings.py`
- `src/ui/__init__.py`
- `src/ui/main_window.py`
- `tests/__init__.py`
- `ИНСТРУКЦИЯ.md`
- `КОМАНДЫ.md`

## Затронутые темы
- [Разработка GUI](gui.md) — закрыта 2026-11-25; каркасные файлы переданы в тему «Реализация шага №2», проверить при возобновлении.

## Связи
- 2026-11-24 [Разработка GUI](gui.md): README обновлён под актуальную структуру/Poetry — проверить, не нужно ли дополнить описание при изменении структуры.
- 2026-11-24 [Разработка GUI](gui.md): затронуты `docs/handoff.md`, `docs/topics/INDEX.md` при фиксации прогресса темы — проверить актуальность при следующем старте.
- 2026-11-24 [Разработка GUI](gui.md): затронуты `main.py`, `src/core/config.py`, `src/core/settings.py`, `src/ui/main_window.py` при подготовке каркаса под тестовый образец — проверить при возвращении к теме.
- 2026-11-25 [Реализация шага №2](../step_2.md): тема закрыта, `main.py`, `src/core/config.py`, `src/ui/main_window.py`, `docs/topics/INDEX.md`, `docs/handoff.md` переданы в новую тему — проверить при возобновлении.
