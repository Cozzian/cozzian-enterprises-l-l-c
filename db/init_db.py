#!/usr/bin/env python3
"""
Cozzian Enterprises LLC — Database Initialiser
==============================================
Creates an SQLite database (cozzian.db) from schema.sql,
seeds it with sample data from seed.sql, then prints row counts
for every table to confirm everything loaded correctly.
"""

import sqlite3
import sys
from pathlib import Path

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / "cozzian.db"
SCHEMA_PATH = DB_DIR / "schema.sql"
SEED_PATH = DB_DIR / "seed.sql"


def run_script(cursor: sqlite3.Cursor, script: str, label: str) -> None:
    """Execute a multi-statement SQL script, splitting on ';' to handle triggers."""
    for statement in script.split(";"):
        stmt = statement.strip()
        if stmt and not stmt.startswith("--"):
            try:
                cursor.execute(stmt)
            except sqlite3.Error as e:
                print(f"  ⚠  Error in {label}: {e}")
                print(f"     Statement: {stmt[:120]}...")


def get_row_counts(cursor: sqlite3.Cursor) -> dict[str, int]:
    """Return {table_name: row_count} for all user tables in the DB."""
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
    )
    tables = [row[0] for row in cursor.fetchall()]
    counts = {}
    for tbl in tables:
        cursor.execute(f"SELECT COUNT(*) FROM [{tbl}]")
        counts[tbl] = cursor.fetchone()[0]
    return counts


def main() -> int:
    # --- 1. Load SQL files -------------------------------------------------
    if not SCHEMA_PATH.exists():
        print(f"❌ Schema file not found: {SCHEMA_PATH}")
        return 1
    if not SEED_PATH.exists():
        print(f"❌ Seed file not found: {SEED_PATH}")
        return 1

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    seed_sql = SEED_PATH.read_text(encoding="utf-8")

    # --- 2. Remove old database so we start fresh -------------------------
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"🧹 Removed existing database: {DB_PATH}")

    # --- 3. Connect & build ------------------------------------------------
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    cursor = conn.cursor()

    print(f"\n{'='*60}")
    print("  Cozzian Enterprises — Database Initialiser")
    print(f"{'='*60}\n")

    # --- 4. Run schema ----------------------------------------------------
    print("📦 Creating schema...")
    run_script(cursor, schema_sql, "schema")
    conn.commit()

    # --- 5. Run seed ------------------------------------------------------
    print("🌱 Seeding data...")
    run_script(cursor, seed_sql, "seed")
    conn.commit()

    # --- 6. Print row counts -----------------------------------------------
    print("\n📊 Row counts after seeding:\n")
    counts = get_row_counts(cursor)
    total = 0
    for tbl, cnt in counts.items():
        padding = " " * (30 - len(tbl))
        print(f"    🗂️  {tbl}{padding}{cnt:>4} row(s)")
        total += cnt

    print(f"\n    ─────────────────────────────────────")
    print(f"    📈 TOTAL rows across all tables:     {total:>4}")
    print(f"\n    ✅ Database ready: {DB_PATH.resolve()}")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())