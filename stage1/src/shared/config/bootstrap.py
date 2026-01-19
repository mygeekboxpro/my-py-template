import os
import logging

from pathlib import Path
from dotenv import load_dotenv, dotenv_values

from shared.logging import configure_logging

_ENV_READY = False

def project_root() -> Path:
    # Adjust if your file layout differs.
    return Path(__file__).resolve().parents[3]

def _env_path() -> Path:
    env_path = project_root() / ".env"
    return env_path

def init_app(*, load_env: bool = True) -> None:
    """
    Initializes process-wide concerns exactly once:
    - load .env
    - configure logging
    """
    global _ENV_READY
    if _ENV_READY:
        return

    if load_env:
        load_dotenv()

    configure_logging()
    _ENV_READY = True

    logger = logging.getLogger(__name__)

    if os.environ.get("ENV_TYPE").lower() == "development":
        env_vars: list[tuple[str, str]] = []
        for key, value in dotenv_values(_env_path()).items():
            env_vars.append((key, value))
        logger.info("bootstrapping.env",
                    extra={"env_vars_len": len(env_vars)})


def require_env(name: str) -> str:
    """
    Fail fast if an expected env var is missing.
    """
    environment = os.environ.get("ENV_TYPE").lower()
    val = os.getenv(name)

    if not val or (environment != "development" and val in {"changeme"}):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return val
