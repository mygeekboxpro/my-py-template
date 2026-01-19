""""
    🧠 Design Rules This Follows (Important)
    ✅ One JSON object per log event
    ✅ No newlines inside message
    ✅ Formatter owns presentation
    ✅ ContextVars over globals
    ✅ Safe for async + MCP + agent loops


    ✅ How to Use
        1️⃣ Initialize once (app startup)
            import logging
            from logging_setup import setup_json_logging, set_correlation_id

            setup_json_logging(logging.INFO, service_name="travel-planner")

            set_correlation_id()  # generate per request / run

        2️⃣ Log anywhere (no coupling)
            import logging

            logger = logging.getLogger(__name__)

            logger.info("orchestrator.started")

        3️⃣ Enable Dev Spacing (Local Only)
            export LOG_PRETTY=true

        4️⃣ Exception Logging (Correct Way)
            try:
                1 / 0
            except Exception:
                logger.exception("calculation.failed")

            Automatically emits:
             - stack trace
             - exception type
             - message
             - correlation_id
"""

import logging
import os
import sys
import uuid
import json
from contextvars import ContextVar
from pythonjsonlogger import json
from pythonjsonlogger.json import JsonFormatter

# ------------------------------------------------------------------------------
# Context (safe for async / agentic systems)
# ------------------------------------------------------------------------------

correlation_id_ctx: ContextVar[str | None] = ContextVar(
    "correlation_id", default=None
)


def set_correlation_id(value: str | None = None) -> str:
    """
    Set or generate a correlation ID for the current execution context.
    """
    cid = value or str(uuid.uuid4())
    correlation_id_ctx.set(cid)
    return cid


# ------------------------------------------------------------------------------
# Formatters
# ------------------------------------------------------------------------------

class PrettyConsoleFormatter(logging.Formatter):
    """
    Human-readable formatter for local development.
    """

    def format(self, record: logging.LogRecord) -> str:
        base = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        cid = correlation_id_ctx.get()
        if cid:
            base["correlation_id"] = cid

        if record.exc_info:
            base["exception"] = self.formatException(record.exc_info)

        pretty = json.dumps(base, indent=2)
        return pretty + "\n"


# ------------------------------------------------------------------------------
# Custom JSON Formatter
# ------------------------------------------------------------------------------

class StructuredJsonFormatter(JsonFormatter):
    """
    JSON formatter with:
    - correlation_id
    - exception info
    - optional dev spacing
    """

    def __init__(self, *args, add_blank_line: bool = False, **kwargs):
        # IMPORTANT: do not pass add_blank_line to super()
        super().__init__(*args, **kwargs)
        self.add_blank_line = add_blank_line

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Standard fields
        log_record["level"] = record.levelname
        log_record["logger"] = record.name

        # Correlation ID (safe even if not set)
        cid = correlation_id_ctx.get()
        if cid:
            log_record["correlation_id"] = cid

    def format(self, record):
        msg = super().format(record)
        return msg + ("\n" if self.add_blank_line else "")


# ------------------------------------------------------------------------------
# Public Setup Function
# ------------------------------------------------------------------------------

def setup_json_logging(
        level: int = logging.INFO,
        *,
        service_name: str | None = None,
) -> None:
    """
    Configure root logger for structured JSON logging.

    Environment variables:
    - LOG_MODE=json    -> default, production-safe

    - LOG_PRETTY=true  -> adds blank line between logs (dev only)
    - LOG_MODE=pretty  -> local development
    """

    log_mode = os.getenv("LOG_MODE", "json").lower()
    add_spacing = os.getenv("LOG_PRETTY", "false").lower() == "true"

    handler = logging.StreamHandler(sys.stderr)

    if log_mode == "pretty":
        handler.setFormatter(PrettyConsoleFormatter())
    else:
        handler.setFormatter(
            StructuredJsonFormatter(add_blank_line=add_spacing)
        )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    if service_name:
        root = logging.getLogger()
        root = logging.LoggerAdapter(root, {"service": service_name})

# Next:
# 🔗 OpenTelemetry span injection
# 📊 Cost / token logging per LLM call
# 🔐 PII-safe redaction filter
# 🧪 pytest log capture helpers
# 📁 Per-module log level overrides
