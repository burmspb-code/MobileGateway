"""HTTP-клиент для проверки соединения с сервером."""

from dataclasses import dataclass

import httpx

from src.core.config import ConnectionSettings


@dataclass
class HealthCheckResult:
    ok: bool
    status_code: int | None
    message: str


class ApiClient:
    async def check_health(self, settings: ConnectionSettings) -> HealthCheckResult:
        normalized = settings.normalized()
        errors = normalized.validate()
        if errors:
            return HealthCheckResult(ok=False, status_code=None, message=errors[0])

        url = normalized.health_check_url
        headers = {}
        if normalized.api_token:
            headers["Authorization"] = f"Bearer {normalized.api_token}"

        try:
            async with httpx.AsyncClient(
                timeout=normalized.timeout,
                follow_redirects=True,
            ) as client:
                response = await client.get(url, headers=headers)
        except httpx.TimeoutException:
            return HealthCheckResult(
                ok=False,
                status_code=None,
                message=f"Таймаут после {normalized.timeout:g} сек",
            )
        except httpx.InvalidURL:
            return HealthCheckResult(
                ok=False,
                status_code=None,
                message="Некорректный адрес сервера",
            )
        except httpx.RequestError:
            return HealthCheckResult(
                ok=False,
                status_code=None,
                message="Не удалось подключиться: проверьте адрес и сеть",
            )
        except Exception:
            return HealthCheckResult(
                ok=False,
                status_code=None,
                message="Неожиданная ошибка при проверке соединения",
            )

        if 200 <= response.status_code < 300:
            return HealthCheckResult(
                ok=True,
                status_code=response.status_code,
                message=f"Соединение установлено ({response.status_code})",
            )

        return HealthCheckResult(
            ok=False,
            status_code=response.status_code,
            message=f"Сервер ответил ошибкой ({response.status_code})",
        )