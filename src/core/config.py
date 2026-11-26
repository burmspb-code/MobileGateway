import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Загружаем переменные из локального файла .env (если он существует в корне проекта).
# В упакованном мобильном приложении find_dotenv() может выбросить AssertionError,
# поэтому ошибку загрузки .env безопасно игнорируем — используются значения по умолчанию.
try:
    load_dotenv()
except Exception:
    pass


@dataclass
class ConnectionSettings:
    """Пользовательские настройки подключения к серверу."""

    api_url: str = ""
    api_token: str = ""
    health_endpoint: str = "/health"
    timeout: float = 10.0

    def normalized(self) -> "ConnectionSettings":
        endpoint = self.health_endpoint.strip() or "/health"
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        return ConnectionSettings(
            api_url=self.api_url.strip().rstrip("/"),
            api_token=self.api_token.strip(),
            health_endpoint=endpoint,
            timeout=self.timeout,
        )

    def validate(self) -> list[str]:
        errors: list[str] = []
        url = self.api_url.strip()
        if not url:
            errors.append("Укажите адрес сервера.")
        elif not (url.startswith("http://") or url.startswith("https://")):
            errors.append("Адрес сервера должен начинаться с http:// или https://.")

        endpoint = self.health_endpoint.strip() or "/health"
        if not endpoint.startswith("/"):
            endpoint = "/" + endpoint
        if " " in endpoint:
            errors.append("Endpoint проверки не должен содержать пробелы.")

        if self.timeout <= 0:
            errors.append("Таймаут должен быть больше 0.")
        if self.timeout > 60:
            errors.append("Таймаут не должен превышать 60 секунд.")

        return errors

    @property
    def health_check_url(self) -> str:
        normalized = self.normalized()
        if not normalized.api_url:
            return ""
        return f"{normalized.api_url}{normalized.health_endpoint}"


@dataclass(frozen=True)
class Settings:
    # Основная информация о приложении
    app_title: str = "Mobile Gateway"
    app_version: str = "0.1.0"

    # Сетевые настройки (адрес вашего сервера)
    api_url: str = os.getenv("API_URL", "http://192.168.1.100:8000")
    api_timeout: float = float(os.getenv("API_TIMEOUT", "10.0"))

    # Настройки мультимедиа и камер
    stream_url: str = os.getenv("STREAM_URL", "")
    snapshot_endpoint: str = os.getenv("SNAPSHOT_ENDPOINT", "/camera/snapshot")

    # Авторизация (если сервер использует токен или API-ключ)
    api_token: str = os.getenv("API_TOKEN", "")

    @property
    def full_snapshot_url(self) -> str:
        """Возвращает полный адрес для получения снимка с сервера."""
        base = self.api_url.rstrip("/")
        path = self.snapshot_endpoint.lstrip("/")
        return f"{base}/{path}"


# Единый объект настроек, который импортируется во все модули проекта
settings = Settings()