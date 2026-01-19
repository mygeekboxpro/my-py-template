from __future__ import annotations

import os
from dataclasses import dataclass
from bootstrap import require_env


@dataclass(frozen=True)
class AppConfig:
    environment: str
    log_mode: str
    log_pretty: str

    openai_api_key: str
    openai_model: str

    gateway_url: str
    http_timeout_secs: int

    app_db_path: str
    tenant_id: str


def load_config() -> AppConfig:
    env = require_env(os.getenv("ENV_TYPE"))
    log_mode = require_env(os.getenv("LOG_MODE"))
    log_pretty = require_env(os.getenv("LOG_PRETTY"))

    openai_api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    openai_model = os.environ.get("OPENAI_MODEL", "gpt-5.2").strip()

    gateway_url = (require_env(os.environ.get("GATEWAY_URL",
                                              "http://127.0.0.1:8080/mcp"))
                   .strip())
    http_timeout_secs = int(require_env(os.environ.get("HTTP_TIMEOUT_SECS",
                                                       30)))

    app_db_path = (require_env(os.environ.get("APP_DB_PATH",
                                              "./data/app.db"))
                   .strip())
    tenant_id = (require_env(os.environ.get("TENANT_ID", "tenant_demo"))
                 .strip())

    return AppConfig(
        environment=env,
        log_mode=log_mode,
        log_pretty=log_pretty,
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        gateway_url=gateway_url,
        http_timeout_secs=http_timeout_secs,
        app_db_path=app_db_path,
        tenant_id=tenant_id,
    )
