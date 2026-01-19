import logging

from shared.config.bootstrap import init_app
from shared.config.app_context_singleton import (
    AppContextHolder,
    load_config
)

logger = logging.getLogger(__name__)


def main():
    ctx = AppContextHolder().get()
    logger.info("ctx", extra={"ctx": str(ctx)})


if __name__ == '__main__':
    init_app()
    AppContextHolder.set(load_config(name="john doe"))
    main()
