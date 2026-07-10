"""Persistência do recorde (highscore) em SQLite, armazenado em %LocalAppData%."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

from snake_game.logger_config import get_logger

logger = get_logger(__name__)


def _get_db_path() -> Path:
    """Retorna o caminho do arquivo SQLite, criando o diretório se necessário."""
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local"))
    else:
        base = str(Path.home() / ".local" / "share")

    db_dir = Path(base) / "SnakeGame"
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / "snake_game.db"


class ScoreRepository:
    """Responsável por ler e gravar o recorde do jogador no SQLite."""

    def __init__(self, db_path: Path | None = None) -> None:
        self._db_path = db_path or _get_db_path()
        self._ensure_schema()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path)

    def _ensure_schema(self) -> None:
        try:
            with self._connect() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS high_scores (
                        id INTEGER PRIMARY KEY CHECK (id = 1),
                        score INTEGER NOT NULL DEFAULT 0
                    )
                    """
                )
                conn.execute(
                    "INSERT OR IGNORE INTO high_scores (id, score) VALUES (1, 0)"
                )
        except sqlite3.Error:
            logger.exception("Falha ao inicializar o banco de dados de recordes.")

    def get_high_score(self) -> int:
        try:
            with self._connect() as conn:
                cursor = conn.execute(
                    "SELECT score FROM high_scores WHERE id = ?", (1,)
                )
                row = cursor.fetchone()
                return row[0] if row else 0
        except sqlite3.Error:
            logger.exception("Falha ao ler o recorde do banco de dados.")
            return 0

    def update_high_score(self, score: int) -> None:
        try:
            with self._connect() as conn:
                conn.execute(
                    "UPDATE high_scores SET score = ? WHERE id = ? AND score < ?",
                    (score, 1, score),
                )
        except sqlite3.Error:
            logger.exception("Falha ao atualizar o recorde no banco de dados.")
