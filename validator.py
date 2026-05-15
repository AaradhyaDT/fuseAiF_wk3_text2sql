"""
validator.py — SQL safety validation

Blocks any non-SELECT statement before it reaches the database.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Forbidden SQL keywords that mutate state
BLOCKED_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|REPLACE|MERGE"
    r"|EXEC|EXECUTE|CALL|GRANT|REVOKE|COPY|VACUUM|REINDEX)\b",
    re.IGNORECASE,
)

# Must start with SELECT (after stripping comments/whitespace)
SELECT_PATTERN = re.compile(r"^\s*(--[^\n]*\n\s*)*SELECT\b", re.IGNORECASE)


def is_safe(sql: str) -> tuple[bool, str]:
    """
    Validate that sql is a safe read-only SELECT query.

    Returns:
        (is_valid: bool, reason: str)
    """
    if not sql or not sql.strip():
        return False, "Empty query"

    # Strip leading SQL comments for the SELECT check
    stripped = re.sub(r"--[^\n]*\n", "", sql).strip()

    if not SELECT_PATTERN.match(stripped):
        return False, "Query must start with SELECT"

    match = BLOCKED_KEYWORDS.search(sql)
    if match:
        return False, f"Blocked keyword detected: {match.group().upper()}"

    # Reject semicolons mid-query (SQL injection via stacking)
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    if len(statements) > 1:
        return False, "Multiple statements not allowed"

    return True, "OK"
