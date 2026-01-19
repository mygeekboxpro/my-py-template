from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbConnFactory:
    db_path: str

    def connect(self) -> sqlite3.Connection:
        (Path(self.db_path)
         .parent
         .mkdir(parents=True, exist_ok=True))
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
