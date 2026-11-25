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
