# Task 1 — Part 2: Text-to-SQL Evaluation Framework

**Assignment:** FUSE AI Fellowship 2026 — Week 3 — GenAI  
**Date:** May 17, 2026  
**Benchmark:** 50 NL Questions from classicmodels PostgreSQL Database

---

## 1. Executive Summary

This evaluation framework defines the methodology, metrics, and procedures for assessing Text-to-SQL systems against the 50-question benchmark dataset. The framework emphasizes **execution accuracy** (result correctness) over exact SQL matching, recognizes the role of self-correction through retries, and provides difficulty-stratified analysis to identify areas of strength and weakness.

---

## 2. Evaluation Dimensions

### 2.1 Execution Success Rate (ESR)

**Definition:** Percentage of generated SQL queries that execute without database errors.

$$\text{ESR} = \frac{\text{Queries that execute without DB error}}{\text{Total queries}} \times 100$$

**What it measures:** Whether the SQL is syntactically valid and executable. A query that returns wrong results still counts as successful for ESR.

**Acceptable threshold:** > 80%

---

### 2.2 Exact SQL Match (EM)

**Definition:** Percentage of generated SQL queries that match the ground truth SQL token-for-token.

$$\text{EM} = \frac{\text{Exact token matches with ground truth}}{\text{Total queries}} \times 100$$

**Limitation:** SQL has multiple equivalent formulations. `SELECT a, b FROM t` and `SELECT b, a FROM t` are semantically identical but fail exact match. Use as a secondary signal only.

**Acceptable threshold:** > 40% (not the primary metric)

---

### 2.3 Execution Accuracy (EA) — *PRIMARY METRIC*

**Definition:** Percentage of queries where the generated SQL returns the **same result set** as the ground truth SQL.

$$\text{EA} = \frac{\text{Queries with result\_set == ground\_truth\_result\_set}}{\text{Total queries}} \times 100$$

**What it measures:** Semantic correctness. This is the only metric that matters from a user perspective—do they get the right answer?

**Comparison rules:**
- Compare result row counts AND values
- For unordered queries (no ORDER BY in ground truth), sort both results before comparison
- Handle NULLs consistently (NULL == NULL)
- For floating-point results, use tolerance (e.g., 0.01 for monetary amounts)

**Acceptable threshold:** > 70% | **Good:** > 80% | **Excellent:** > 90%

---

### 2.4 Component-Level Accuracy

Break down correctness at the SQL clause level to identify which types of operations the system struggles with:

| Component | Check | Scoring |
|-----------|-------|---------|
| **Table Selection** | Are correct tables referenced? | Binary: 0 or 1 |
| **Column Selection** | Are correct columns projected? | Binary: 0 or 1 |
| **JOIN Correctness** | Are tables joined on correct keys? | Binary: 0 or 1 |
| **Filter Correctness** | Does WHERE clause match intent? | Binary: 0 or 1 |
| **Aggregation** | Are COUNT/SUM/AVG/etc. used correctly? | Binary: 0 or 1 |
| **GROUP BY** | Is correct grouping applied? | Binary: 0 or 1 |
| **ORDER BY** | Are results ordered correctly? | Binary: 0 or 1 |

**Calculation:** Average the binary score across all queries per component.

**Example:** If 45/50 queries have correct table selection → Table Selection Accuracy = 90%

**Purpose:** Identifies which SQL features the system is weak in, directing improvement efforts.

---

### 2.5 Retry / Self-Correction Success Rate

**Definition:** Percentage of initially-failed queries that are successfully fixed after retry.

$$\text{Recovery Rate} = \frac{\text{Queries fixed after retry}}{\text{Queries that failed initially}} \times 100$$

**What it measures:** The agent's resilience and ability to learn from error messages.

**Task 3 context:** Max 1 retry per query  
**Task 4 context:** Max 3 retries per query

**Acceptable threshold:** > 40% | **Good:** > 60%

---

### 2.6 Query Generation Latency

**Definition:** Time from question input to final answer delivery.

**Metrics to track:**
- **Average latency (ms):** Mean across all 50 queries
- **Median latency (ms):** Middle value
- **P95 latency (ms):** 95th percentile (tail performance)
- **P99 latency (ms):** Worst-case performance

**Breakdown (if logging permits):**
- LLM decomposition time (ms)
- LLM SQL generation time (ms)
- DB query execution time (ms)
- Total round-trip time (ms)

**Acceptable threshold:** Avg < 5s | **Good:** Avg < 2s | **Excellent:** Avg < 1s

---

### 2.7 Natural Language Answer Quality

**Definition:** Quality of the final summary sentence presented to the user.

**Evaluation criteria (qualitative, human spot-checks):**

| Criterion | Score |
|-----------|-------|
| **Factual Correctness** | Does it match the result data? |
| **Completeness** | Does it fully answer the question? |
| **Clarity** | Is it readable and concise (< 2 sentences)? |
| **Grammar** | No spelling or grammatical errors? |

**Scoring:** Rate 1–5 on each criterion for a sample of 5–10 queries.  
**Acceptable:** Average > 3.5 / 5

---

## 3. Evaluation Protocol

### 3.1 Pre-Evaluation Setup

1. **Load benchmark questions** from `sql_questions_only.csv` or hard-coded list
2. **Execute all ground truth queries** (from Task1_Part1_Ground_Truth.md)
3. **Store expected results** as baseline for comparison
4. **Initialize evaluation log** (JSON Lines format)

### 3.2 Per-Query Evaluation Loop

For each of the 50 questions:

```
1. START_TIME = current_time
2. question = get_question(i)
3. generated_sql = agent.generate(question)
4. IS_VALID = validate(generated_sql)
   - If not valid: status = "validation_failed", skip to logging
5. execution_result = try_execute(generated_sql)
   - If error: 
       * If Task 3: status = "failed_execution"
       * If Task 4: retry_count += 1
         - If retry_count <= max_retries: go to step 3 (regenerate)
         - Else: status = "max_retries_exceeded"
6. result_match = compare_results(execution_result, expected_result)
7. LATENCY_MS = current_time - START_TIME
8. Log all metrics
9. Return status
```

### 3.3 Result Comparison Algorithm

```python
def results_match(generated, expected):
    if generated.row_count != expected.row_count:
        return False
    if not same_column_set(generated.columns, expected.columns):
        return False
    # Normalize: sort rows if no ORDER BY in expected
    gen_rows = sort_rows(generated.rows)
    exp_rows = sort_rows(expected.rows)
    for gen_row, exp_row in zip(gen_rows, exp_rows):
        for gen_val, exp_val in zip(gen_row, exp_row):
            if gen_val != exp_val:  # handle NULLs correctly
                return False
    return True
```

---

## 4. Logging and Reporting

### 4.1 Per-Query Log Entry (JSON)

```json
{
  "query_index": 1,
  "question": "List all products",
  "ground_truth_sql": "SELECT * FROM products;",
  "generated_sql": "SELECT * FROM products;",
  "is_valid_sql": true,
  "execution_success": true,
  "result_match": true,
  "retry_count": 0,
  "retry_used": false,
  "latency_ms": 145,
  "timestamp": "2026-05-17T10:30:00Z",
  "status": "success",
  "error": null
}
```

### 4.2 Aggregate Metrics Report

```
=== EVALUATION SUMMARY ===
Total Queries Tested:            50
Execution Success Rate (ESR):    92.0%
Exact SQL Match Rate (EM):       58.0%
Execution Accuracy (EA):         78.0%
Retry Rate:                       12.0% (6/50 queries retried)
Retry Success Rate:              66.7% (4/6 fixed)
Avg Latency (ms):                285
P95 Latency (ms):                512
P99 Latency (ms):                784

=== COMPONENT BREAKDOWN ===
Table Selection Accuracy:        95%
Column Selection Accuracy:       92%
JOIN Correctness:                85%
Filter Correctness:              88%
Aggregation Correctness:         72%
GROUP BY Correctness:            78%

=== DIFFICULTY BREAKDOWN ===
Easy (Q1-Q20):       EA = 92%, ESR = 98%
Medium (Q21-Q40):    EA = 78%, ESR = 92%
Hard (Q41-Q50):      EA = 54%, ESR = 82%

=== FAILURE ANALYSIS ===
Syntax Errors:                   4 (8.0%)
Wrong Table/Column Name:         3 (6.0%)
Missing JOIN:                    2 (4.0%)
Incorrect Aggregation:           7 (14.0%)
DML Blocked:                     0 (0.0%)
All Retries Exhausted:           2 (4.0%)
```

### 4.3 Per-Question Results Table

| # | Question | Generated SQL | Executed | Correct | Retry | Status | Latency |
|---|----------|---------------|----------|---------|-------|--------|---------|
| 1 | List all products | SELECT * FROM products; | ✓ | ✓ | No | Success | 120ms |
| 2 | Get all customers | SELECT * FROM customers; | ✓ | ✓ | No | Success | 135ms |
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## 5. Scoring Formula

### 5.1 Overall Text-to-SQL Performance Score

$$\text{Overall Score} = 0.40 \times \text{ESR} + 0.40 \times \text{EA} + 0.20 \times \text{Recovery Rate}$$

**Interpretation:**
- **80–100:** Excellent (production-ready)
- **70–80:** Good (minor issues, acceptable)
- **60–70:** Acceptable (significant issues, needs work)
- **<60:** Poor (system not ready)

### 5.2 Component Accuracy Average

$$\text{Component Score} = \frac{\sum \text{(Table + Column + JOIN + Filter + Aggregation + GROUP BY)}}{6}$$

Identifies which areas need optimization.

---

## 6. Failure Categories to Track

| Category | Definition | Action |
|----------|-----------|--------|
| **Syntax Error** | Generated SQL has syntax errors | Log error message, count as execution failure |
| **Wrong Table Name** | Referenced non-existent table or misnamed table | Log as component failure (Table Selection) |
| **Wrong Column Name** | Referenced non-existent or wrong column | Log as component failure (Column Selection) |
| **Missing JOIN** | Should have joined 2+ tables but didn't | Log as JOIN failure, inspect decomposition |
| **Incorrect Aggregation** | Wrong aggregate function (COUNT vs SUM) | Log as aggregation failure |
| **Incorrect GROUP BY** | Missing or wrong grouping column | Log as GROUP BY failure |
| **DML Blocked** | Generated UPDATE/DELETE/INSERT | Validator caught it; count as validation failure |
| **Retry Succeeded** | First attempt failed, but retry fixed it | Count as recovery success, log retry count |
| **Max Retries Exhausted** | Tried max times, still failed | Log as unrecoverable failure |
| **Timeout** | Query took > 10s to execute | Log as latency failure, don't retry |

---

## 7. Difficulty Classification

Queries categorized by SQL complexity:

### Easy (Q1–Q20)
- Single table, no JOINs
- Simple SELECT, DISTINCT, or basic filtering
- No aggregation or GROUP BY
- Expected EA > 95%

**Questions:** Q1–Q20 (simple SELECT queries)

### Medium (Q21–Q40)
- 2 tables, 1–2 JOINs
- Aggregation (COUNT, SUM) or GROUP BY
- Basic filtering with WHERE
- Expected EA > 80%

**Questions:** Q21–Q40 (JOINs + aggregation queries)

### Hard (Q41–Q50)
- 3+ tables or complex logic
- Multiple aggregations
- Subqueries or self-joins
- Expected EA > 70%

**Questions:** Q41–Q50 (complex aggregates + self-joins)

Report metrics separately by difficulty to understand agent performance across complexity levels.

---

## 8. Benchmark Constraints & Ground Truth Validation

### 8.1 Database Schema
- **Database:** classicmodels (PostgreSQL)
- **Tables:** 8 (productlines, products, offices, employees, customers, payments, orders, orderdetails)
- **Rows:** ~13,000 across all tables
- **Key constraint:** All camelCase column names must be double-quoted

### 8.2 Ground Truth Validation
- All 50 ground truth SQL queries have been manually verified
- Results documented in `Task1_Part1_Ground_Truth.md`
- Baseline results stored in `task1_ground_truth_results.json`
- All queries are SELECT-only; no DML operations

### 8.3 Test Environment
- PostgreSQL 15+
- Docker-compose setup with seeded database
- Timezone-aware timestamp handling

---

## 9. Evaluation Workflow Timeline

```
Day 1: Setup
  ├─ Deploy database + seed data
  ├─ Load all ground truth queries and results
  └─ Initialize evaluation framework

Day 2: Task 3 Evaluation
  ├─ Run all 50 questions through Task 3 pipeline
  ├─ Collect metrics and logs
  ├─ Generate evaluation report
  └─ Identify bottlenecks (retry patterns, error types)

Day 3: Task 4 Evaluation
  ├─ Run all 50 questions through Task 4 agent
  ├─ Collect metrics with up-to 3 retries per query
  ├─ Compare against Task 3 baseline
  └─ Generate final evaluation report
```

---

## 10. Success Criteria

For **Task 3 (Pipeline)**:
- [ ] ESR ≥ 80%
- [ ] EA ≥ 60%
- [ ] Avg latency < 5s
- [ ] Evaluation report generated with all metrics

For **Task 4 (Agent)**:
- [ ] ESR ≥ 85%
- [ ] EA ≥ 70%
- [ ] Recovery rate ≥ 50% (using up to 3 retries)
- [ ] Avg latency < 3s
- [ ] NL answer quality ≥ 3.5/5

---

## 11. References & Best Practices

### Industry Benchmarks
- **Spider:** Yale Text-to-SQL benchmark (138 databases, 10,181 questions)
- **BIRD:** Complex cross-domain SQL generation (12,751 questions)
- **WikiSQL:** Basic single-table queries (80,654 questions)

### Evaluation Papers
- Zhong et al. (2020): "Grounded Logical Nets"
- Yu et al. (2018): "SParC—Semantic Parsing in Context"
- Finegan-Dollak et al. (2018): "Improving Text-to-SQL Evaluation Methodology"

### Key Insight
**Result-based evaluation (EA) is superior to string matching (EM)** because:
1. Multiple valid SQL formulations exist
2. Only the result matters to the user
3. Order independence reflects actual database semantics

---

**Document Version:** 1.0  
**Last Updated:** May 17, 2026  
**Feedback / Revisions:** Use ground truth results from Task1_Part1_Ground_Truth.md as baseline

