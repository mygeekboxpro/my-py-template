from __future__ import annotations

from dataclasses import dataclass
from shared.config.bootstrap import init_app, require_env
from shared.constants import llm_constants


@dataclass(frozen=True)
class AppContext:
    environment: str
    log_mode: str
    log_pretty: str

    openai_api_key: str
    openai_model: str

    gateway_url: str
    http_timeout_secs: int

    app_db_path: str
    tenant_id: str


# PROCESS-WIDE CONTEXT
# AppContext → immutable data container
# AppContextHolder → singleton-style access
# Context is:
#  - built once in main()
#  - read anywhere via AppContextHolder.get()
# Good for single process, single user, no per-request state, batch jobs etc.
# Not good for Multiple concurrent requests, Async execution, web servers etc.
#

# Replace AppContextHolder with contextvars.ContextVar
# It gives:
#   - Request isolation
#   - async safety
#   - zero signature pollution


class AppContextHolder:
    _ctx: AppContext | None = None

    @classmethod
    def set(cls, ctx: AppContext) -> None:
        # This prevents silent overwrites.
        if cls._ctx is not None:
            raise RuntimeError("AppContext already set")
        cls._ctx = ctx

    @classmethod
    def get(cls) -> AppContext:
        if cls._ctx is None:
            raise RuntimeError(f"AppContext has not been set.")
        return cls._ctx

    # useful in tests
    @classmethod
    def clear(cls) -> None:
        cls._ctx = None


def load_config(name: str) -> AppContext:
    env = require_env("ENV_TYPE").strip()
    log_mode = require_env("LOG_MODE").strip()
    log_pretty = require_env("LOG_PRETTY").strip()
    gateway_url = require_env("GATEWAY_URL").strip()
    openai_api_key = require_env("OPENAI_API_KEY").strip()
    http_timeout_secs = int(require_env("HTTP_TIMEOUT_SECONDS").strip())
    app_db_path = require_env("APP_DB_PATH").strip()
    tenant_id = require_env("TENANT_ID").strip()

    openai_model = llm_constants.OPENAI_MODEL_GPT_4O_MINI.strip()

    return AppContext(
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
