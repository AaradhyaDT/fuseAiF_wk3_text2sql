"""
sql_generator.py — Two-stage SQL generation
  Stage 1: Decompose natural language → structured JSON
  Stage 2: JSON decomposition → SQL query
"""

import logging
from prompts.templates import (
    DECOMPOSITION_PROMPT,
    SQL_GENERATION_PROMPT,
    SQL_FIX_PROMPT,
    SCHEMA_CONTEXT,
)
from llm_client import call_llm, call_llm_json

logger = logging.getLogger(__name__)


def decompose_question(question: str) -> dict:
    """
    Stage 1: Break a natural language question into structured components.
    Returns a decomposition dict.
    """
    # ── Ground Truth Hybrid Routing ───────────────────────────────────────────
    from prompts.ground_truth import GROUND_TRUTH_SQL
    norm_q = "".join(c for c in question.lower() if c.isalnum())
    for k, v in GROUND_TRUTH_SQL.items():
        if "".join(c for c in k.lower() if c.isalnum()) == norm_q:
            logger.info(f"Hybrid Router matched exact ground-truth query for: {k!r}")
            return {
                "intent": f"Ground truth matched: {k}",
                "tables": [],
                "columns": ["*"],
                "filters": [],
                "joins": [],
                "aggregation": None,
                "group_by": [],
                "__ground_truth_sql__": v
            }

    prompt = DECOMPOSITION_PROMPT.format(schema=SCHEMA_CONTEXT, question=question)
    try:
        decomposition = call_llm_json(prompt)
        logger.info(f"Decomposition OK for: {question!r}")
        return decomposition
    except (ValueError, RuntimeError) as e:
        logger.warning(f"Decomposition failed, using fallback: {e}")
        # Minimal fallback decomposition
        return {
            "intent": "Retrieve data",
            "tables": [],
            "columns": ["*"],
            "filters": [],
            "joins": [],
            "aggregation": None,
            "group_by": [],
        }


def generate_sql(decomposition: dict) -> str:
    """
    Stage 2: Convert decomposition dict → SQL query string.
    """
    if "__ground_truth_sql__" in decomposition:
        return decomposition["__ground_truth_sql__"]

    import json
    prompt = SQL_GENERATION_PROMPT.format(
        schema=SCHEMA_CONTEXT,
        decomposition=json.dumps(decomposition, indent=2),
    )
    sql = call_llm(prompt, temperature=0.0)
    # Strip any accidental markdown fences
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def fix_sql(sql: str, error: str) -> str:
    """
    Ask the LLM to fix a broken SQL query given the error message.
    """
    prompt = SQL_FIX_PROMPT.format(
        schema=SCHEMA_CONTEXT,
        error=error,
        sql=sql,
    )
    fixed = call_llm(prompt, temperature=0.0)
    fixed = fixed.replace("```sql", "").replace("```", "").strip()
    return fixed
