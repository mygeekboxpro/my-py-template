import contextvars
import logging
import uuid

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="")
logger = logging.getLogger(__name__)


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        rid = request_id_var.get()
        record.request_id = rid if rid else None
        return True


def set_request_id(value: str | None = None) -> str:
    rid = value or str(uuid.uuid4())
    request_id_var.set(rid)
    return rid


def add_request_id_filter() -> None:
    logging.getLogger().addFilter(RequestIdFilter())


# ---- usage ----
add_request_id_filter()

rid = set_request_id()  # set once per request
logger.info("handling request", extra={"route": "/tools/call"})
logger.info("calling tool", extra={"tool": "search_flights"})
