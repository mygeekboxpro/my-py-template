from __future__ import annotations

import os
import json
import logging
import sys
from datetime import datetime, timezone
from pythonjsonlogger.json import JsonFormatter

_RESERVED_LOG_RECORD_ATTRS = {
    "name", "msg", "args", "levelname", "levelno", "pathname", "filename",
    "module", "exc_info", "exc_text", "stack_info", "lineno", "funcName",
    "created", "msecs", "relativeCreated", "thread", "threadName",
    "processName", "process", "message"
}


def _base_payload(record: logging.LogRecord) -> dict:
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "level": record.levelname,
        "logger": record.name,
        "module": record.module,
        "func": record.funcName,
        "line": record.lineno,
        "msg": record.getMessage(),
    }

    if record.exc_info:
        # logging.Formatter.formatException expects exc_info tuple
        payload["exc_info"] = logging.Formatter().formatException(
            record.exc_info)

    # Add fields passed via extra={...}
    for k, v in record.__dict__.items():
        if k.startswith("_"):
            continue
        if k in _RESERVED_LOG_RECORD_ATTRS:
            continue
        payload[k] = v

    return payload


class StructuredJsonFormatter(JsonFormatter):
    def __init__(self, *args, add_blank_line: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self._add_blank_line = add_blank_line

    def format(self, record: logging.LogRecord) -> str:
        payload = _base_payload(record)
        out = json.dumps(payload, ensure_ascii=False)

        if self._add_blank_line:
            return out + "\n"

        return out


class PrettyConsoleFormatter(logging.Formatter):
    """Human-readable formatter for local development."""

    def format(self, record: logging.LogRecord) -> str:
        payload = _base_payload(record)
        pretty = json.dumps(payload, ensure_ascii=False, indent=2)
        return "\n" + pretty


def configure_logging(level: int = logging.INFO) -> None:
    """
    Logging setup.

    Env vars:
    - LOG_MODE=json|pretty   (default: json)
    - LOG_PRETTY=true|false  (adds blank line spacing for JSON mode; default: false)
    """
    log_mode = os.getenv("LOG_MODE", "json").lower()
    add_spacing = os.getenv("LOG_PRETTY", "false").lower() == "true"

    handler = logging.StreamHandler(sys.stderr)

    if log_mode == "pretty":
        handler.setFormatter(PrettyConsoleFormatter())
    else:
        handler.setFormatter(
            StructuredJsonFormatter(add_blank_line=add_spacing))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)
