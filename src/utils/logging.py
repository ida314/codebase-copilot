"""Logging utilities for the project."""

import logging as _log
import os, sys

_CONFIGURED = False
_FMT = "%(asctime)s | %(levelname)s | %(name)s:%(lineno)d — %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

def configure(level: str | int | None = None) -> None:
    """Idempotent setup. Uses LOG_LEVEL env if provided."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    if isinstance(level, str):
        level = level.upper()

    env_level = os.getenv("LOG_LEVEL", "")
    lvl = (
        _log._nameToLevel.get(env_level.upper())
        or _log._nameToLevel.get(level)  # type: ignore[arg-type]
        or _log.INFO
    )

    root = _log.getLogger()
    root.setLevel(lvl)

    # Avoid duplicate handlers (e.g., in reloaders)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = _log.StreamHandler(sys.stdout)
    handler.setLevel(lvl)
    handler.setFormatter(_log.Formatter(_FMT, datefmt=_DATEFMT))
    root.addHandler(handler)

    _CONFIGURED = True

def get_logger(name: str | None = None) -> _log.Logger:
    """Project-wide accessor. Auto-configures on first call."""
    if not _CONFIGURED:
        configure()
    return _log.getLogger(name or "app")
