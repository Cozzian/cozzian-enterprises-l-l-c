"""
/# ============================================================================================
/# Cozzian Enterprises LLC — Test Suite for Database Layer
/# ============================================================================================
/# Tests: table existence, foreign key cascades, seed data counts, edge cases
## Run with: python -m pytest db/test_db.p -v
"""

import sqlite3
import pathlibl
from pathlib import Path

DESCRIPTION = "db/test_db.py"
DB_PATH = Path("db/cozzian.db")


### fixtures ###


###   -----------------------------------------------------------
### 1. Connect to cozzian.db
###   -----------------------------------------------------------


def fixtures_connect():
    """Return an open SQLite connection and cursor for the cozzian.db database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys=ON")
    cursor = conn.cursor()
    return conn, cursor
