from dataclasses import dataclass
from contextvars import ContextVar


# WHAT the contexts is   → AppContext (dataclass)
# WHERE it lives        → ContextVar

# AppContext → immutable data container
@dataclass(frozen=True)
class AppContext:
    name: str
    summary: str
    profile: str
    system_prompt: str
    evaluator_system_prompt: str


# ContextVar → request / task scoped access
_app_ctx: ContextVar[AppContext] = ContextVar("app_ctx")


def set_ctx(ctx: AppContext) -> None:
    _app_ctx.set(ctx)


def get_ctx() -> AppContext:
    try:
        return _app_ctx.get()
    except LookupError:
        raise RuntimeError("AppContext has not been set")
