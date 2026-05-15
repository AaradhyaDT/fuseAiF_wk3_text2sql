"""
database.py — PostgreSQL connection and safe query execution
"""

import psycopg2
import psycopg2.extras
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ── Connection config — update with your actual credentials ──────────────────
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "classicmodels",   # change to your DB name
    "user": "postgres",            # change to your user
    "password": "password",        # change to your password
}


def get_connection():
    """Return a live psycopg2 connection."""
    return psycopg2.connect(**DB_CONFIG)


def execute_query(sql: str, timeout_ms: int = 10_000) -> dict:
    """
    Execute a single SQL query safely.

    Returns:
        {
            "columns": [...],
            "rows": [...],
            "row_count": int,
            "execution_time_ms": float,
            "error": None | str
        }
    """
    start = time.perf_counter()
    result = {
        "columns": [],
        "rows": [],
        "row_count": 0,
        "execution_time_ms": 0.0,
        "error": None,
    }

    try:
        with get_connection() as conn:
            # Set statement timeout so runaway queries don't hang
            with conn.cursor() as cur:
                cur.execute(f"SET statement_timeout = {timeout_ms};")

            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                result["columns"] = list(rows[0].keys()) if rows else []
                result["rows"] = [dict(r) for r in rows]
                result["row_count"] = len(rows)

    except Exception as e:
        result["error"] = str(e)
        logger.error(f"Query execution error: {e}\nSQL: {sql}")

    result["execution_time_ms"] = round((time.perf_counter() - start) * 1000, 2)
    return result


def test_connection() -> bool:
    """Ping the database."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return True
    except Exception as e:
        logger.error(f"DB connection failed: {e}")
        return False
