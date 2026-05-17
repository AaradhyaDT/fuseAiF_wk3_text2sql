# Week 3 — Task Plan: Text-to-SQL & Agentic Query System
**Assignment:** Week3_Problem_Set_GenAI | **Due:** 20 May | **Points:** 100
**Database:** classicmodels (PostgreSQL) | **Benchmark:** 50 NL questions (sql_questions_only.csv)

---

## Overview

Four sequential tasks that build on each other:

```
Task 1 → Ground truth SQL + Evaluation design
Task 2 → Manual query decomposition
Task 3 → Automated Text-to-SQL pipeline (prompt chaining, vanilla Python)
Task 4 → Mini SQL Agent (FastAPI, agentic retry loop)
```

All tasks reuse the same PostgreSQL database seeded with `seed.sql`.

---

## Database Schema Reference

**8 tables** (classicmodels-style, all column names quoted camelCase):

| Table | Key Columns |
|---|---|
| `productlines` | `productLine` (PK) |
| `products` | `productCode` (PK), `productLine` (FK), `buyPrice`, `MSRP`, `quantityInStock` |
| `offices` | `officeCode` (PK), `city`, `country` |
| `employees` | `employeeNumber` (PK), `officeCode` (FK), `reportsTo` (self-FK) |
| `customers` | `customerNumber` (PK), `salesRepEmployeeNumber` (FK→employees), `country`, `creditLimit` |
| `payments` | `customerNumber`+`checkNumber` (PK), `amount`, `paymentDate` |
| `orders` | `orderNumber` (PK), `customerNumber` (FK), `status`, `orderDate` |
| `orderdetails` | `orderNumber`+`productCode` (PK), `quantityOrdered`, `priceEach` |

> **Critical:** All column names must be double-quoted in queries (e.g., `"customerNumber"`, `"productLine"`).

---

## Task 1: SQL Benchmark Dataset Preparation & Evaluation Design

### Goal
Write correct ground-truth SQL for all 50 benchmark questions. Design an evaluation framework for Text-to-SQL systems.

### Deliverables
- Document: one section per question → NL question + SQL + result screenshot + explanation
- Separate document: evaluation framework write-up

---

### Part 1 — Ground Truth SQL Queries

Below are all 50 questions from `sql_questions_only.csv` with their SQL solutions.

#### Simple SELECT (Q1–Q20)

**Q1. List all products**
```sql
SELECT * FROM products;
```

**Q2. Get all customers**
```sql
SELECT * FROM customers;
```

**Q3. Show all orders**
```sql
SELECT * FROM orders;
```

**Q4. List all employees**
```sql
SELECT * FROM employees;
```

**Q5. Get all offices**
```sql
SELECT * FROM offices;
```

**Q6. Show all product lines**
```sql
SELECT * FROM productlines;
```

**Q7. List all payments**
```sql
SELECT * FROM payments;
```

**Q8. Get product names and prices**
```sql
SELECT "productName", "buyPrice", "MSRP"
FROM products;
```

**Q9. Get customer names and cities**
```sql
SELECT "customerName", city
FROM customers;
```

**Q10. List employee first and last names**
```sql
SELECT "firstName", "lastName"
FROM employees;
```

**Q11. Get all order dates**
```sql
SELECT "orderNumber", "orderDate"
FROM orders;
```

**Q12. Show product vendor list**
```sql
SELECT DISTINCT "productVendor"
FROM products;
```

**Q13. Get all product codes**
```sql
SELECT "productCode"
FROM products;
```

**Q14. List all countries from offices**
```sql
SELECT DISTINCT country
FROM offices;
```

**Q15. Show all order statuses**
```sql
SELECT DISTINCT status
FROM orders;
```

**Q16. Get all payment amounts**
```sql
SELECT "checkNumber", amount, "paymentDate"
FROM payments;
```

**Q17. List all job titles**
```sql
SELECT DISTINCT "jobTitle"
FROM employees;
```

**Q18. Get customer phone numbers**
```sql
SELECT "customerName", phone
FROM customers;
```

**Q19. Show product MSRP values**
```sql
SELECT "productName", "MSRP"
FROM products;
```

**Q20. List order numbers**
```sql
SELECT "orderNumber"
FROM orders;
```

---

#### JOIN Queries (Q21–Q30)

**Q21. Get orders with customer names**
```sql
SELECT o."orderNumber", o."orderDate", c."customerName"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```

**Q22. Get employees with office city**
```sql
SELECT e."firstName", e."lastName", of.city
FROM employees e
JOIN offices of ON e."officeCode" = of."officeCode";
```

**Q23. Get payments with customer names**
```sql
SELECT c."customerName", p."checkNumber", p.amount, p."paymentDate"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```

**Q24. Get order details with product names**
```sql
SELECT od."orderNumber", pr."productName", od."quantityOrdered", od."priceEach"
FROM orderdetails od
JOIN products pr ON od."productCode" = pr."productCode";
```

**Q25. Get products with product line description**
```sql
SELECT pr."productName", pl."textDescription"
FROM products pr
JOIN productlines pl ON pr."productLine" = pl."productLine";
```

**Q26. Get customers with sales rep names**
```sql
SELECT c."customerName", e."firstName" || ' ' || e."lastName" AS "salesRepName"
FROM customers c
JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber";
```

**Q27. Get orders with customer city**
```sql
SELECT o."orderNumber", o."orderDate", c.city
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```

**Q28. Get employees and their manager**
```sql
SELECT e."firstName" || ' ' || e."lastName" AS employee,
       m."firstName" || ' ' || m."lastName" AS manager
FROM employees e
LEFT JOIN employees m ON e."reportsTo" = m."employeeNumber";
```

**Q29. Get order details with product vendor**
```sql
SELECT od."orderNumber", pr."productVendor", od."quantityOrdered"
FROM orderdetails od
JOIN products pr ON od."productCode" = pr."productCode";
```

**Q30. Get payments with customer country**
```sql
SELECT p."checkNumber", p.amount, c.country
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```

---

#### Aggregation Queries (Q31–Q40)

**Q31. Count customers per country**
```sql
SELECT country, COUNT("customerNumber") AS customer_count
FROM customers
GROUP BY country
ORDER BY customer_count DESC;
```

**Q32. Total payments per customer**
```sql
SELECT c."customerName", SUM(p.amount) AS total_paid
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY total_paid DESC;
```

**Q33. Number of orders per status**
```sql
SELECT status, COUNT("orderNumber") AS order_count
FROM orders
GROUP BY status;
```

**Q34. Products per product line**
```sql
SELECT "productLine", COUNT("productCode") AS product_count
FROM products
GROUP BY "productLine"
ORDER BY product_count DESC;
```

**Q35. Employees per office**
```sql
SELECT of.city, COUNT(e."employeeNumber") AS employee_count
FROM employees e
JOIN offices of ON e."officeCode" = of."officeCode"
GROUP BY of.city
ORDER BY employee_count DESC;
```

**Q36. Total stock per product vendor**
```sql
SELECT "productVendor", SUM("quantityInStock") AS total_stock
FROM products
GROUP BY "productVendor"
ORDER BY total_stock DESC;
```

**Q37. Average buy price per product line**
```sql
SELECT "productLine", ROUND(AVG("buyPrice"), 2) AS avg_buy_price
FROM products
GROUP BY "productLine"
ORDER BY avg_buy_price DESC;
```

**Q38. Orders per customer**
```sql
SELECT c."customerName", COUNT(o."orderNumber") AS order_count
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY order_count DESC;
```

**Q39. Max MSRP per product line**
```sql
SELECT "productLine", MAX("MSRP") AS max_msrp
FROM products
GROUP BY "productLine";
```

**Q40. Min buy price per vendor**
```sql
SELECT "productVendor", MIN("buyPrice") AS min_buy_price
FROM products
GROUP BY "productVendor";
```

---

#### Single-Value Aggregate Queries (Q41–Q50)

**Q41. Total number of customers**
```sql
SELECT COUNT("customerNumber") AS total_customers
FROM customers;
```

**Q42. Total number of products**
```sql
SELECT COUNT("productCode") AS total_products
FROM products;
```

**Q43. Total revenue from payments**
```sql
SELECT SUM(amount) AS total_revenue
FROM payments;
```

**Q44. Average product price**
```sql
SELECT ROUND(AVG("buyPrice"), 2) AS avg_buy_price
FROM products;
```

**Q45. Max payment amount**
```sql
SELECT MAX(amount) AS max_payment
FROM payments;
```

**Q46. Min payment amount**
```sql
SELECT MIN(amount) AS min_payment
FROM payments;
```

**Q47. Count total orders**
```sql
SELECT COUNT("orderNumber") AS total_orders
FROM orders;
```

**Q48. Total quantity in stock**
```sql
SELECT SUM("quantityInStock") AS total_stock
FROM products;
```

**Q49. Average MSRP**
```sql
SELECT ROUND(AVG("MSRP"), 2) AS avg_msrp
FROM products;
```

**Q50. Number of employees**
```sql
SELECT COUNT("employeeNumber") AS total_employees
FROM employees;
```

---

### Part 2 — Evaluation Framework

**Document title:** "Text-to-SQL Evaluation Framework"

Structure the document with these sections:

#### 1. Evaluation Dimensions

| Dimension | Description | Metric |
|---|---|---|
| Execution Success | Does the SQL run without error? | % queries executed |
| Exact SQL Match | Does generated SQL match ground truth exactly? | Exact match % |
| Result Accuracy | Does output match expected rows/values? | Result match % |
| Table Selection | Are the correct tables used? | Precision/Recall |
| Column Selection | Are the correct columns selected? | Precision/Recall |
| Join Correctness | Are JOINs on correct keys? | Binary per query |
| Filter Correctness | Are WHERE/HAVING conditions right? | Binary per query |
| Retry Success | Did self-correction fix failed queries? | Retry success % |
| Latency | How fast is query generation? | Avg ms per query |
| NL Answer Quality | Is the natural language summary sensible? | Manual 1–5 score |

#### 2. Evaluation Protocol
- Run all 50 benchmark questions through the system
- Compare results against ground-truth SQL results (not SQL text — result sets)
- Log: generated SQL, execution status, result rows, retry count, latency
- Produce a per-question report table + aggregate metrics

#### 3. Scoring Formula
```
Overall Score = 0.4 × Execution Rate + 0.4 × Result Accuracy + 0.2 × Retry Success Rate
```

#### 4. Failure Categories to Track
- Syntax error (unresolvable)
- Wrong table/column name
- Missing JOIN
- Incorrect aggregation
- DML blocked by validator
- Retry succeeded
- All retries exhausted

---

## Task 2: Query Decomposition

### Goal
For each of the 50 benchmark questions, manually decompose the question into structured components before writing SQL.

### Format per question
```
Question: <NL question>
- Intent: <what is being retrieved/computed>
- Tables: <tables involved>
- Columns: <columns needed>
- Filters: <WHERE/HAVING conditions, if any>
- Joins: <join conditions, if any>
- Aggregation: <GROUP BY / aggregate function, if any>
```

### Sample Decompositions (representative set)

**Q1. List all products**
- Intent: Retrieve all product records
- Tables: products
- Columns: all (*)
- Filters: None
- Joins: None
- Aggregation: None

**Q21. Get orders with customer names**
- Intent: Retrieve orders joined with customer info
- Tables: orders, customers
- Columns: orderNumber, orderDate, customerName
- Filters: None
- Joins: orders.customerNumber = customers.customerNumber
- Aggregation: None

**Q31. Count customers per country**
- Intent: Count how many customers exist in each country
- Tables: customers
- Columns: country, COUNT(customerNumber)
- Filters: None
- Joins: None
- Aggregation: GROUP BY country

**Q38. Orders per customer**
- Intent: Count orders per customer
- Tables: orders, customers
- Columns: customerName, COUNT(orderNumber)
- Filters: None
- Joins: orders.customerNumber = customers.customerNumber
- Aggregation: GROUP BY customerName

**Q28. Get employees and their manager**
- Intent: Show each employee alongside their reporting manager
- Tables: employees (self-join)
- Columns: employee full name, manager full name
- Filters: None
- Joins: employees.reportsTo = employees.employeeNumber (LEFT JOIN for CEO who has no manager)
- Aggregation: None

> Complete all 50 in the submission document following this same format.

---

## Task 3: Text-to-SQL Pipeline (Prompt Chaining)

### Goal
Build a vanilla Python prompt-chaining system with Streamlit UI. No LangChain/LangGraph.

### Project Structure
```
project/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── database.py
├── sql_generator.py
├── validator.py
├── executor.py
├── prompts/
│   ├── __init__.py
│   └── templates.py
├── logs/
│   └── query_logs.json
├── evaluate.py
└── streamlit_app.py
```

### Implementation Steps

#### Step 1 — Environment & Docker setup
- `docker-compose.yml`: PostgreSQL (port 5432) + Streamlit (port 8501)
- PostgreSQL init: mount `seed.sql` as init script
- `.env.example`: `DATABASE_URL`, `OPENAI_API_KEY`

#### Step 2 — `database.py`
- `get_connection()` → psycopg2 connection from `DATABASE_URL`
- `execute_query(sql) → list[dict]` — returns rows as dicts, raises on error

#### Step 3 — `prompts/templates.py`
Three prompt templates:
- `DECOMPOSE_PROMPT` — extract Intent/Tables/Columns/Filters/Joins as JSON
- `GENERATE_PROMPT` — given decomposition + schema, write PostgreSQL SELECT
- `FIX_PROMPT` — given broken SQL + error message, return corrected SQL

#### Step 4 — `sql_generator.py`
Three functions each making one OpenAI API call:
- `decompose(question) → dict`
- `generate_sql(decomposition) → str`
- `fix_sql(sql, error) → str`

#### Step 5 — `validator.py`
- `validate(sql) → bool`
- Blocks: `DELETE`, `DROP`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`
- Only passes `SELECT` queries

#### Step 6 — `executor.py`
Orchestrates the full pipeline:
```
question → decompose → generate → validate → execute
                                               ↓ (on error)
                                             fix → execute (once)
                                               ↓ (on error)
                                             return failed status
```
Returns: `{"question", "sql", "result", "status", "retry_needed"}`

#### Step 7 — `streamlit_app.py`
- Chat input box
- Displays: generated SQL (code block), retry indicator, result table
- Session state for chat history

#### Step 8 — `evaluate.py`
- Loads benchmark questions (from CSV or hardcoded list)
- Runs each through the pipeline
- Outputs console table: Question | Generated SQL | Executed | Correct | Retry | Status
- Prints aggregate metrics at end

### Key Rules
- SELECT only — validator must block all DML/DDL
- Max 1 retry per query
- Every execution logged to `logs/query_logs.json` with timestamp, question, sql, status, latency_ms
- System must not crash on errors — all exceptions caught and returned as `status: "failed"`

### LLM Configuration
- Model: `gpt-4o-mini`
- Temperature: 0 (deterministic SQL generation)
- Library: `openai` (standard, not LangChain)

### Evaluation Output Format
```
Question                        | Generated SQL      | Executed | Correct | Retry | Status
--------------------------------|--------------------|----------|---------|-------|--------
List all products               | SELECT * FROM ...  | Yes      | Yes     | No    | Success
Count customers per country     | SELECT country...  | Yes      | Yes     | No    | Success
Get employees and their manager | SELECT e.first...  | No       | Fixed   | Yes   | Success
...

=== Metrics ===
Execution Success Rate : XX%
Retry Success Rate     : XX%
Total Failed Queries   : X / 50
```

---

## Task 4: Mini SQL Agent (FastAPI)

### Goal
Build a FastAPI agentic endpoint with state-based workflow, up to 3 retries, and NL summarization.

### Project Structure
```
app/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── agents/
│   ├── __init__.py
│   ├── executor.py
│   ├── llm.py
│   ├── planner.py
│   ├── sql_generator.py
│   ├── summarizer.py
│   └── validator.py
├── graph/
│   ├── __init__.py
│   └── workflow.py
├── prompts/
│   └── __init__.py
├── sql/
│   └── seed.sql
├── tools/
│   ├── __init__.py
│   └── db_tools.py
├── __init__.py
├── config.py
├── db.py
├── main.py
└── streamlit_app.py
```

### Agent State (dataclass)
```python
@dataclass
class AgentState:
    user_query: str
    plan: dict | None = None
    generated_sql: str | None = None
    is_valid_sql: bool = False
    execution_results: list[dict] | None = None
    final_answer: str | None = None
    errors: list[str] = field(default_factory=list)
    retry_count: int = 0
    status: str = "pending"
```

### Agent Workflow (`graph/workflow.py`)
```
user_query
    │
    ▼
[Planner] → plan (tables, intent, strategy)
    │
    ▼
[SQL Generator] → generated_sql
    │
    ▼
[Validator] → is_valid_sql
    │ No → back to Generator with error feedback (max 3 loops)
    │ Yes
    ▼
[Executor] → execution_results
    │ Error → back to Generator with DB error (counts as retry)
    │ OK
    ▼
[Summarizer] → final_answer
    │
    ▼
FastAPI Response
```

### Agent Responsibilities

**`agents/planner.py`** — LLM call: analyze query + schema → structured plan JSON
```json
{
  "intent": "Count shipped orders from USA customers",
  "tables": ["orders", "customers"],
  "strategy": "Join orders and customers on customerNumber, filter status=Shipped and country=USA, apply COUNT"
}
```

**`agents/sql_generator.py`** — LLM call: plan + schema → PostgreSQL SELECT query

**`agents/validator.py`** — Rule-based: block DML/DDL, verify SELECT-only

**`agents/executor.py`** — Run SQL via `db_tools.py`, catch errors, return rows

**`agents/summarizer.py`** — LLM call: original question + result rows → natural language answer

**`agents/llm.py`** — Centralized OpenAI client, single `call_llm(system, user, model)` function

### FastAPI Endpoint (`main.py`)
```
POST /agent/sql
Content-Type: application/json

Request:  { "question": "How many shipped orders are from USA customers?" }

Response: {
  "sql": "SELECT COUNT(*) FROM orders o JOIN customers c ...",
  "result": 42,
  "summary": "There are 42 shipped orders from customers in USA.",
  "status": "success"
}
```

### Error & Retry Logic
- Max 3 retries
- Each retry: pass failed SQL + DB error message back to SQL Generator
- After 3 failures: return `status: "failed"`, `summary: "Unable to answer after 3 attempts."`
- All retries logged

### Logging Requirements (per request)
```json
{
  "timestamp": "2026-05-17T10:30:00",
  "question": "...",
  "plan": {...},
  "generated_sql": "...",
  "retry_count": 0,
  "execution_time_ms": 142,
  "status": "success"
}
```

### `config.py`
Load from `.env`:
- `DATABASE_URL`
- `OPENAI_API_KEY`
- `MODEL_NAME` (default: `gpt-4o-mini`)

### Streamlit UI (`streamlit_app.py`)
- Chat interface → calls `/agent/sql` endpoint
- Shows: plan, SQL, result table, NL summary, retry count

### Evaluation Against Benchmark
Run all 50 questions from `sql_questions_only.csv` through `POST /agent/sql`. Report:
- Execution success rate
- Retry rate
- Failed queries
- Average latency per query

---

## Submission Checklist

### Task 1
- [ ] Document with all 50 NL questions + SQL + result screenshots + explanations
- [ ] Evaluation framework document

### Task 2
- [ ] Document with all 50 decompositions (Intent / Tables / Columns / Filters / Joins / Aggregation)

### Task 3
- [ ] Full source code (all files in `project/`)
- [ ] `logs/query_logs.json` (populated from evaluation run)
- [ ] Evaluation report table (console output or exported)
- [ ] Short architecture write-up (1 page max)
- [ ] At least 2 successful query case examples
- [ ] At least 1 failed + retry case example

### Task 4
- [ ] Full source code (all files in `app/`)
- [ ] Working `POST /agent/sql` endpoint
- [ ] Logs from benchmark run
- [ ] Evaluation results against the 50-question dataset

---

## Recommended Execution Order

```
Day 1
  ├─ Set up PostgreSQL locally (seed.sql already available)
  ├─ Complete Task 1 Part 1: write + run all 50 SQL queries, capture results
  └─ Write Task 1 Part 2: evaluation framework document

Day 2
  ├─ Complete Task 2: decompositions for all 50 questions
  └─ Start Task 3: scaffold project/, docker-compose, database.py

Day 3
  ├─ Complete Task 3: prompts, sql_generator, validator, executor, streamlit_app
  └─ Run evaluate.py against benchmark, save logs

Day 4
  ├─ Build Task 4: agent state, workflow, FastAPI endpoint
  ├─ Add summarizer and retry logic
  └─ Run benchmark evaluation, finalize all submission documents
```

---

## Common Pitfalls to Avoid

- **Quoting:** All camelCase column names need double quotes in PostgreSQL — `"customerNumber"`, not `customerNumber`
- **Self-join in Q28:** Use `LEFT JOIN` not `INNER JOIN` or the CEO (who has no manager) is excluded
- **Task 3 retry:** Exactly 1 retry allowed; Task 4 allows up to 3 — don't mix these up
- **Validator:** Must check for DML keywords case-insensitively (`delete`, `DELETE`, `Delete` all blocked)
- **Logging:** Must log even failed queries — the log is part of the submission
- **Docker init:** PostgreSQL `POSTGRES_DB` env var + mounting `seed.sql` to `/docker-entrypoint-initdb.d/` is the standard pattern to auto-seed on container start
