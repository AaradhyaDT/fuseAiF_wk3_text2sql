"""
database.py — PostgreSQL connection and safe query execution
"""

import os
import psycopg
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# ── Connection config — read from environment variables with sane defaults ──
# Update these environment variables instead of hardcoding credentials:
#   DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "classicmodels"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}


def get_connection():
    """Return a live psycopg (psycopg3) connection."""
    # psycopg.connect returns a connection usable as a context manager
    return psycopg.connect(**DB_CONFIG)


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

            # Use dict row factory to get rows as mappings
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
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
