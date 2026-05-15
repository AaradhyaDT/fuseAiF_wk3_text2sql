# Task 1 — Part 2: Evaluation Strategy for Text-to-SQL Systems

## Overview

A Text-to-SQL agent must be evaluated at **three layers**:
execution validity, result correctness, and answer quality.
No single metric captures all three.

---

## Evaluation Dimensions

### 1. Execution Success Rate (ESR)

**What it measures:** Does the generated SQL actually run without errors?

```
ESR = (Queries that execute without DB error) / (Total queries) × 100
```

A query that runs but returns wrong results still counts as a success here.
This is the bare minimum bar.

---

### 2. Exact Match (EM)

**What it measures:** Is the generated SQL token-for-token identical to the
ground truth SQL?

```
EM = (Exact matches) / (Total queries) × 100
```

**Limitation:** SQL has many valid ways to express the same query.
`SELECT a, b FROM t` and `SELECT b, a FROM t` are semantically equivalent
but won't match exactly. Use EM only as a secondary signal.

---

### 3. Execution Accuracy (EA) — *Most important metric*

**What it measures:** Does the generated SQL return the same result set
as the ground truth SQL?

```
EA = (Queries where result_set == ground_truth_result_set) / Total × 100
```

Compare row counts AND values. Order-independent comparison for SELECT queries
without ORDER BY.

**Why this matters:** This is the metric that reflects whether the agent is
actually correct — not just syntactically valid.

---

### 4. Component-Level Accuracy

Break down correctness at the SQL clause level:

| Component | Check |
|-----------|-------|
| Table selection | Correct tables referenced? |
| Column selection | Correct columns projected? |
| JOIN correctness | Right tables joined on right keys? |
| Filter correctness | WHERE clause matches intent? |
| Aggregation | COUNT/SUM/AVG used correctly? |
| GROUP BY | Correct grouping applied? |

Score each component independently (0 or 1 per query per component),
then average across the dataset.

---

### 5. Retry / Self-Correction Success Rate

**What it measures:** When the first attempt fails, does the agent recover?

```
Recovery Rate = (Queries fixed after retry) / (Queries that failed initially) × 100
```

Tracks the agent's resilience, not just raw accuracy.

---

### 6. Query Generation Latency

Track time from question input to final result:

- Average latency (ms)
- P95 latency (tail performance)
- Breakdown: LLM decomposition + LLM generation + DB execution

---

### 7. Natural Language Answer Quality (Qualitative)

For the final summary sentence, evaluate:

- **Factual correctness:** Does it match the result data?
- **Completeness:** Does it answer the full question?
- **Clarity:** Is it readable and concise?

Use human spot-checks on a sample (5–10 per run) rather than automated scoring.

---

## Evaluation Benchmark Framework

### Dataset Structure

```
benchmark_dataset.csv columns:
  question          → natural language question
  ground_truth_sql  → manually verified correct SQL
  expected_result   → serialized expected result (JSON)
  difficulty        → easy / medium / hard
  tags              → [aggregation, join, filter, subquery, ...]
```

### Evaluation Pipeline

```
For each question in benchmark:
  1. Run agent → get generated_sql + result
  2. Execute ground_truth_sql → get expected_result
  3. Compute:
       - executed_ok   = (generated_sql ran without error)
       - result_match  = (result == expected_result)
       - retry_used    = (agent retried)
       - latency_ms    = end_time - start_time
  4. Log all metrics to evaluation_report.jsonl
```

### Final Report Template

| Question | Generated SQL | Executed | Result Correct | Retry | Status | Latency |
|----------|---------------|----------|----------------|-------|--------|---------|
| Count customers in USA | SELECT COUNT(*) FROM customers WHERE country='USA' | ✓ | ✓ | No | Success | 420ms |
| Orders from Germany | SELECT ... | ✓ | ✗ | Yes → Fixed | Success | 870ms |

---

## Difficulty Classification

| Level | Characteristics |
|-------|-----------------|
| Easy | Single table, no joins, simple filters |
| Medium | 2 tables, 1 join, aggregation or GROUP BY |
| Hard | 3+ tables, subqueries, complex conditions, edge cases |

Report metrics separately by difficulty level to understand where the agent
breaks down.

---

## Recommended Minimum Acceptable Thresholds

| Metric | Acceptable | Good | Excellent |
|--------|-----------|------|-----------|
| Execution Success Rate | >80% | >90% | >95% |
| Execution Accuracy (EA) | >60% | >75% | >85% |
| Recovery Rate (retries) | >40% | >60% | >80% |
| Avg Latency | <5s | <2s | <1s |

---

## References

- Spider benchmark (Yale): standard Text-to-SQL evaluation dataset
- BIRD benchmark: more complex, real-world queries
- Test-suite evaluation (Zhong et al. 2020): execution-based accuracy
