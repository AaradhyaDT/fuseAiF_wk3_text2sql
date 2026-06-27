"""
executor.py — Safe SQL execution with retry and logging
"""

import logging
import time
from database import execute_query
from validator import is_safe
from sql_generator import fix_sql

logger = logging.getLogger(__name__)


def run_with_retry(sql: str, max_retries: int = 1) -> dict:
    """
    Validate → Execute → Retry on failure.

    Args:
        sql:         The SQL query string to execute
        max_retries: How many fix-and-retry attempts to allow (Task 3: 1, Task 4: 3)

    Returns:
        {
            "sql": str,            # final SQL attempted
            "result": dict,        # execute_query output
            "attempts": int,
            "retried": bool,
            "status": "success" | "failed" | "blocked"
        }
    """
    response = {
        "sql": sql,
        "result": {},
        "attempts": 0,
        "retried": False,
        "status": "failed",
    }

    current_sql = sql

    for attempt in range(max_retries + 1):
        response["attempts"] = attempt + 1

        # ── Safety gate ──────────────────────────────────────────────────────
        valid, reason = is_safe(current_sql)
        if not valid:
            logger.warning(f"Blocked unsafe SQL: {reason}\nSQL: {current_sql}")
            response["status"] = "blocked"
            response["result"] = {"error": f"Blocked: {reason}", "rows": [], "row_count": 0}
            return response

        # ── Execute ──────────────────────────────────────────────────────────
        logger.info(f"Executing (attempt {attempt + 1}):\n{current_sql}")
        result = execute_query(current_sql)
        response["sql"] = current_sql
        response["result"] = result

        if result["error"] is None:
            response["status"] = "success"
            logger.info(f"Query succeeded in {result['execution_time_ms']}ms, "
                        f"{result['row_count']} rows")
            return response

        # ── Error: retry if attempts remain ──────────────────────────────────
        logger.warning(f"Query failed (attempt {attempt + 1}): {result['error']}")

        if attempt < max_retries:
            logger.info("Asking LLM to fix the query...")
            try:
                current_sql = fix_sql(current_sql, result["error"])
                response["retried"] = True
                logger.info(f"Fixed SQL:\n{current_sql}")
            except Exception as e:
                logger.error(f"LLM fix failed: {e}")
                break

    response["status"] = "failed"
    return response
