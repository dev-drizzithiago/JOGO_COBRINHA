"""Configuração de logging estruturado em JSON para o Jogo da Cobrinha."""
from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any


def _get_log_dir() -> Path:
    """Retorna o diretório de logs, criando-o se necessário (Windows/Linux)."""
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
    else:
        base = str(Path.home() / ".local" / "share")

    log_dir = Path(base) / "SnakeGame" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


class JsonFormatter(logging.Formatter):
    """Formata cada registro de log como uma linha JSON."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def get_logger(name: str = "snake_game") -> logging.Logger:
    """Cria (ou reutiliza) um logger que grava em arquivo JSON."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    log_file = _get_log_dir() / "snake_game.json"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(JsonFormatter())
    logger.addHandler(file_handler)

    return logger
