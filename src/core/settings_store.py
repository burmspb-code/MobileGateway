"""Загрузка/сохранение ConnectionSettings."""

from __future__ import annotations

import json
import os
from pathlib import Path

import flet as ft

from src.core.config import ConnectionSettings


class SettingsStore:
    KEYS = {
        "api_url": "mg.api_url",
        "api_token": "mg.api_token",
        "health_endpoint": "mg.health_endpoint",
        "timeout": "mg.timeout",
    }

    def __init__(self, page: ft.Page):
        self.page = page
        storage_dir = os.getenv("FLET_APP_STORAGE_DATA") or "."
        self._fallback_path = Path(storage_dir) / "connection_settings.json"

    def load(self) -> ConnectionSettings:
        data = self._read_all()
        timeout_raw = data.get(self.KEYS["timeout"], 10.0)
        try:
            timeout = float(timeout_raw)
        except (TypeError, ValueError):
            timeout = 10.0

        settings = ConnectionSettings(
            api_url=str(data.get(self.KEYS["api_url"], "") or ""),
            api_token=str(data.get(self.KEYS["api_token"], "") or ""),
            health_endpoint=str(data.get(self.KEYS["health_endpoint"], "/health") or "/health"),
            timeout=timeout,
        )
        return settings.normalized()

    def save(self, settings: ConnectionSettings) -> None:
        normalized = settings.normalized()
        data = {
            self.KEYS["api_url"]: normalized.api_url,
            self.KEYS["api_token"]: normalized.api_token,
            self.KEYS["health_endpoint"]: normalized.health_endpoint,
            self.KEYS["timeout"]: normalized.timeout,
        }
        self._write_all(data)

    def _read_all(self) -> dict:
        # 1) Пытаемся client_storage (если доступен в этой версии Flet)
        storage = getattr(self.page, "client_storage", None)
        if storage is not None:
            try:
                data = {}
                for key in self.KEYS.values():
                    value = storage.get(key)
                    if value is not None:
                        data[key] = value
                if data:
                    return data
            except Exception:
                pass

        # 2) Fallback: JSON-файл
        try:
            if self._fallback_path.exists():
                return json.loads(self._fallback_path.read_text(encoding="utf-8"))
        except Exception:
            pass
        return {}

    def _write_all(self, data: dict) -> None:
        # 1) Пытаемся client_storage
        storage = getattr(self.page, "client_storage", None)
        if storage is not None:
            try:
                for key, value in data.items():
                    storage.set(key, value)
                return
            except Exception:
                pass

        # 2) Fallback: JSON-файл
        self._fallback_path.parent.mkdir(parents=True, exist_ok=True)
        self._fallback_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )