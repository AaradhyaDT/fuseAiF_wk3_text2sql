"""
main.py — FastAPI application
Exposes:
  POST /pipeline/sql   — Task 3: simple Text-to-SQL pipeline (1 retry)
  POST /agent/sql      — Task 4: full agentic system    (3 retries + summary)
  GET  /health         — connectivity check
  GET  /evaluate       — run benchmark dataset evaluation
"""

import json
import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import test_connection, execute_query
from executor import run_with_retry
from llm_client import call_llm
from prompts.templates import SUMMARY_PROMPT
from prompts.ground_truth import GROUND_TRUTH_SQL
from sql_generator import decompose_question, generate_sql

# ── Logging setup ─────────────────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "app.log"),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text-to-SQL Agent",
    description="AI-powered natural language → SQL system (Fuse AI Fellowship WK3)",
    version="1.0.0",
)


# ── Request / Response models ─────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str


class PipelineResponse(BaseModel):
    question: str
    decomposition: dict
    sql: str
    result: Any
    status: str
    attempts: int
    retried: bool
    execution_time_ms: float


class AgentResponse(BaseModel):
    question: str
    decomposition: dict
    sql: str
    result: Any
    summary: str
    status: str
    attempts: int
    retried: bool
    execution_time_ms: float


# ── Helpers ───────────────────────────────────────────────────────────────────
def _log_query(payload: dict):
    """Append each query run to a JSONL log file."""
    entry = {"timestamp": datetime.utcnow().isoformat(), **payload}
    with open(LOG_DIR / "queries.jsonl", "a") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def _generate_summary(question: str, result: dict) -> str:
    """Ask LLM to convert raw result rows into a human-readable sentence."""
    # Trim result to avoid token bloat
    rows = result.get("rows", [])
    rows_preview = rows[:10]
    row_count = result.get("row_count", len(rows))

    # Provide both total row count and preview to ensure LLM summaries are accurate
    data_payload = {
        "total_rows_matching_query": row_count,
        "data_preview": rows_preview
    }

    prompt = SUMMARY_PROMPT.format(
        question=question,
        result=json.dumps(data_payload, default=str),
    )
    try:
        return call_llm(prompt, temperature=0.2, max_tokens=150)
    except Exception:
        return f"Query returned {row_count} rows."


def _compare_results(gen_res: dict, gt_res: dict, has_order_by: bool) -> bool:
    """
    Compare generated query result against ground truth query result.
    Order-independent by default unless has_order_by is True.
    """
    if gen_res.get("error") or gt_res.get("error"):
        return False

    gen_rows = gen_res.get("rows", [])
    gt_rows = gt_res.get("rows", [])

    if len(gen_rows) != len(gt_rows):
        return False

    if not gen_rows and not gt_rows:
        return True

    # Normalize rows by converting to sorted tuple of key-value string pairs
    def normalize(rows):
        normalized = []
        for r in rows:
            normalized.append(tuple(sorted((k, str(v)) for k, v in r.items())))
        return normalized

    norm_gen = normalize(gen_rows)
    norm_gt = normalize(gt_rows)

    if has_order_by:
        return norm_gen == norm_gt
    else:
        return sorted(norm_gen) == sorted(norm_gt)


# ── Routes ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    db_ok = test_connection()
    return {"status": "ok" if db_ok else "db_error", "db_connected": db_ok}


@app.post("/pipeline/sql", response_model=PipelineResponse)
def pipeline_sql(req: QuestionRequest):
    """
    Task 3: Text-to-SQL pipeline with 1 retry.
    Steps: Decompose → Generate SQL → Validate → Execute (→ Fix → Retry)
    """
    t0 = time.perf_counter()
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"[PIPELINE] Question: {question!r}")

    # Stage 1: decompose
    decomposition = decompose_question(question)
    logger.info(f"[PIPELINE] Decomposition: {decomposition}")

    # Stage 2: generate SQL
    try:
        sql = generate_sql(decomposition)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SQL generation failed: {e}")
    logger.info(f"[PIPELINE] Generated SQL:\n{sql}")

    # Stage 3-5: validate, execute, retry
    exec_result = run_with_retry(sql, max_retries=1)
    total_ms = round((time.perf_counter() - t0) * 1000, 2)

    response = {
        "question": question,
        "decomposition": decomposition,
        "sql": exec_result["sql"],
        "result": exec_result["result"],
        "status": exec_result["status"],
        "attempts": exec_result["attempts"],
        "retried": exec_result["retried"],
        "execution_time_ms": total_ms,
    }
    _log_query(response)
    return response


@app.post("/agent/sql", response_model=AgentResponse)
def agent_sql(req: QuestionRequest, skip_summary: bool = False):
    """
    Task 4: Full mini SQL agent — 3 retries + natural language summary.
    """
    t0 = time.perf_counter()
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    logger.info(f"[AGENT] Question: {question!r}")

    # Step 1: Understand query
    decomposition = decompose_question(question)
    logger.info(f"[AGENT] Decomposition: {decomposition}")

    # Step 2: Generate SQL
    try:
        sql = generate_sql(decomposition)
    except Exception as e:
        fallback = {
            "question": question,
            "decomposition": decomposition,
            "sql": "",
            "result": {"error": str(e), "rows": [], "row_count": 0},
            "summary": "I was unable to generate a SQL query for this question.",
            "status": "failed",
            "attempts": 0,
            "retried": False,
            "execution_time_ms": round((time.perf_counter() - t0) * 1000, 2),
        }
        _log_query(fallback)
        return fallback
    logger.info(f"[AGENT] Generated SQL:\n{sql}")

    # Steps 3-4: Execute with up to 3 retries
    exec_result = run_with_retry(sql, max_retries=3)

    # Step 5: Natural language summary
    if exec_result["status"] == "success":
        if skip_summary:
            summary = f"Query returned {exec_result['result'].get('row_count', 0)} rows."
        else:
            summary = _generate_summary(question, exec_result["result"])
    else:
        summary = (
            f"I was unable to answer this question after "
            f"{exec_result['attempts']} attempt(s). "
            f"Error: {exec_result['result'].get('error', 'unknown')}"
        )

    total_ms = round((time.perf_counter() - t0) * 1000, 2)

    response = {
        "question": question,
        "decomposition": decomposition,
        "sql": exec_result["sql"],
        "result": exec_result["result"],
        "summary": summary,
        "status": exec_result["status"],
        "attempts": exec_result["attempts"],
        "retried": exec_result["retried"],
        "execution_time_ms": total_ms,
    }
    _log_query(response)
    return response


@app.get("/evaluate")
def evaluate_benchmark():
    """
    Run the full benchmark CSV dataset through the agent and return
    an evaluation report (Task 3 & 4 evaluation requirement).
    Calculates both Execution Success Rate (ESR) and Execution Accuracy (EA) against ground-truth.
    """
    import csv

    benchmark_path = Path("sql_questions_only.csv")
    if not benchmark_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Place sql_questions_only.csv in the project root directory",
        )

    with open(benchmark_path) as f:
        reader = csv.DictReader(f)
        questions = [row["question"] for row in reader]

    results = []
    success_count = 0
    correct_count = 0
    retry_count = 0
    failed_count = 0

    for q in questions:
        req = QuestionRequest(question=q)
        try:
            resp = agent_sql(req, skip_summary=True)

            # Fetch ground truth and run it to get expected result for Execution Accuracy (EA)
            gt_sql = GROUND_TRUTH_SQL.get(q)
            is_correct = False
            gt_error = None

            if gt_sql:
                gt_res = execute_query(gt_sql)
                if gt_res["error"]:
                    gt_error = gt_res["error"]
                else:
                    # Compare agent's result against ground-truth result
                    has_order_by = "order by" in gt_sql.lower()
                    is_correct = _compare_results(resp["result"], gt_res, has_order_by)
            else:
                # If no ground truth mapped, default to whether it executed successfully
                is_correct = resp["status"] == "success"

            row = {
                "question": q,
                "generated_sql": resp["sql"] if isinstance(resp, dict) else resp.sql,
                "executed_successfully": (resp["status"] if isinstance(resp, dict) else resp.status) == "success",
                "result_correct": is_correct,
                "retry_needed": resp["retried"] if isinstance(resp, dict) else resp.retried,
                "attempts": resp["attempts"] if isinstance(resp, dict) else resp.attempts,
                "status": resp["status"] if isinstance(resp, dict) else resp.status,
                "summary": resp["summary"] if isinstance(resp, dict) else resp.summary,
                "execution_time_ms": resp["execution_time_ms"] if isinstance(resp, dict) else resp.execution_time_ms,
                "gt_error": gt_error
            }
            if row["executed_successfully"]:
                success_count += 1
            else:
                failed_count += 1
            if row["result_correct"]:
                correct_count += 1
            if row["retry_needed"]:
                retry_count += 1
        except Exception as e:
            row = {
                "question": q,
                "generated_sql": "",
                "executed_successfully": False,
                "result_correct": False,
                "retry_needed": False,
                "attempts": 0,
                "status": "error",
                "summary": str(e),
                "execution_time_ms": 0,
                "gt_error": None
            }
            failed_count += 1

        results.append(row)
        time.sleep(1.0)  # Moderate pacing delay to stay well within Groq rate limits

    total = len(questions)
    return {
        "total_questions": total,
        "success_count": success_count,
        "correct_count": correct_count,
        "failed_count": failed_count,
        "retry_count": retry_count,
        "execution_success_rate": f"{round(success_count / total * 100, 1)}%",
        "execution_accuracy": f"{round(correct_count / total * 100, 1)}%",
        "retry_rate": f"{round(retry_count / total * 100, 1)}%",
        "results": results,
    }


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
