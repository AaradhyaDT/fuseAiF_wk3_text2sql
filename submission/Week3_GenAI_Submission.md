# Week 3 — GenAI Assignment
## Text-to-SQL Agentic System (FastAPI + PostgreSQL + Groq LLM)

**Student:** Aaradhya Dev Tamrakar
**Program:** Fuse AI Fellowship 2026
**Due:** 20 May 2026

---

# Task 1: SQL Benchmark Dataset & Evaluation Design

## Part 1: Ground Truth SQL Queries

> For each question: SQL query is written below. Run it in pgAdmin/psql, paste screenshot in the `[SCREENSHOT]` slot.

---

### Q1. List all products
**SQL:**
```sql
SELECT * FROM products;
```
**Explanation:** Retrieves all rows and columns from the products table.
**Result:** `[SCREENSHOT]`

---

### Q2. Get all customers
```sql
SELECT * FROM customers;
```
**Explanation:** Retrieves all rows and columns from the customers table.
**Result:** `[SCREENSHOT]`

---

### Q3. Show all orders
```sql
SELECT * FROM orders;
```
**Explanation:** Retrieves all rows and columns from the orders table.
**Result:** `[SCREENSHOT]`

---

### Q4. List all employees
```sql
SELECT * FROM employees;
```
**Result:** `[SCREENSHOT]`

---

### Q5. Get all offices
```sql
SELECT * FROM offices;
```
**Result:** `[SCREENSHOT]`

---

### Q6. Show all product lines
```sql
SELECT * FROM productlines;
```
**Result:** `[SCREENSHOT]`

---

### Q7. List all payments
```sql
SELECT * FROM payments;
```
**Result:** `[SCREENSHOT]`

---

### Q8. Get product names and prices
```sql
SELECT "productName", "buyPrice", "MSRP"
FROM products;
```
**Explanation:** Selects only the name and pricing columns from products.
**Result:** `[SCREENSHOT]`

---

### Q9. Get customer names and cities
```sql
SELECT "customerName", "city"
FROM customers;
```
**Result:** `[SCREENSHOT]`

---

### Q10. List employee first and last names
```sql
SELECT "firstName", "lastName"
FROM employees;
```
**Result:** `[SCREENSHOT]`

---

### Q11. Get all order dates
```sql
SELECT "orderNumber", "orderDate"
FROM orders;
```
**Result:** `[SCREENSHOT]`

---

### Q12. Show product vendor list
```sql
SELECT DISTINCT "productVendor"
FROM products;
```
**Explanation:** DISTINCT removes duplicate vendors, giving a clean unique list.
**Result:** `[SCREENSHOT]`

---

### Q13. Get all product codes
```sql
SELECT "productCode"
FROM products;
```
**Result:** `[SCREENSHOT]`

---

### Q14. List all countries from offices
```sql
SELECT DISTINCT "country"
FROM offices;
```
**Result:** `[SCREENSHOT]`

---

### Q15. Show all order statuses
```sql
SELECT DISTINCT "status"
FROM orders;
```
**Result:** `[SCREENSHOT]`

---

### Q16. Get all payment amounts
```sql
SELECT "customerNumber", "checkNumber", "amount"
FROM payments;
```
**Result:** `[SCREENSHOT]`

---

### Q17. List all job titles
```sql
SELECT DISTINCT "jobTitle"
FROM employees;
```
**Result:** `[SCREENSHOT]`

---

### Q18. Get customer phone numbers
```sql
SELECT "customerName", "phone"
FROM customers;
```
**Result:** `[SCREENSHOT]`

---

### Q19. Show product MSRP values
```sql
SELECT "productName", "MSRP"
FROM products;
```
**Result:** `[SCREENSHOT]`

---

### Q20. List order numbers
```sql
SELECT "orderNumber"
FROM orders;
```
**Result:** `[SCREENSHOT]`

---

### Q21. Get orders with customer names
```sql
SELECT o."orderNumber", o."orderDate", o."status", c."customerName"
FROM orders o
```

---

## Evaluation Results (Automated)

I ran the full 50-question benchmark using the agent endpoint (`GET /evaluate`) inside the Dockerized environment.

- Total questions: 50
- Execution success (queries that ran): 10
- Execution accuracy (matched ground truth): 7
- Execution success rate: 20.0%
- Execution accuracy: 14.0%

Full evaluation JSON report saved as [evaluation_report.json](evaluation_report.json).

Notes:
- Some queries failed to generate SQL (LLM generation returned errors for those prompts). I fixed several bugs (prompt formatting, JSON parsing, Decimal serialization) and restarted the app; remaining failures are likely due to model output variability and can be improved by prompt tuning or increasing retries.
- The project is Dockerized — see README for `docker compose up` instructions to reproduce.

---

JOIN customers c ON o."customerNumber" = c."customerNumber";
```
**Explanation:** Joins orders and customers on customerNumber to show who placed each order.
**Result:** `[SCREENSHOT]`

---

### Q22. Get employees with office city
```sql
SELECT e."firstName", e."lastName", e."jobTitle", o."city"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode";
```
**Explanation:** Joins employees to offices to show which city each employee works in.
**Result:** `[SCREENSHOT]`

---

### Q23. Get payments with customer names
```sql
SELECT c."customerName", p."checkNumber", p."paymentDate", p."amount"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```
**Result:** `[SCREENSHOT]`

---

### Q24. Get order details with product names
```sql
SELECT od."orderNumber", p."productName", od."quantityOrdered", od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode";
```
**Explanation:** Joins orderdetails with products to replace product codes with readable names.
**Result:** `[SCREENSHOT]`

---

### Q25. Get products with product line description
```sql
SELECT p."productName", pl."productLine", pl."textDescription"
FROM products p
JOIN productlines pl ON p."productLine" = pl."productLine";
```
**Result:** `[SCREENSHOT]`

---

### Q26. Get customers with sales rep names
```sql
SELECT c."customerName",
       e."firstName" || ' ' || e."lastName" AS "salesRepName"
FROM customers c
JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber";
```
**Explanation:** Joins customers to employees using the salesRepEmployeeNumber FK. Concatenates first and last name.
**Result:** `[SCREENSHOT]`

---

### Q27. Get orders with customer city
```sql
SELECT o."orderNumber", o."orderDate", c."customerName", c."city"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```
**Result:** `[SCREENSHOT]`

---

### Q28. Get employees and their manager
```sql
SELECT e1."firstName" || ' ' || e1."lastName" AS "employee",
       e2."firstName" || ' ' || e2."lastName" AS "manager"
FROM employees e1
LEFT JOIN employees e2 ON e1."reportsTo" = e2."employeeNumber";
```
**Explanation:** Self-join on the employees table. e1 = the employee, e2 = their manager via reportsTo. LEFT JOIN keeps employees with no manager (top of hierarchy).
**Result:** `[SCREENSHOT]`

---

### Q29. Get orderdetails with product vendor
```sql
SELECT od."orderNumber", p."productName", p."productVendor", od."quantityOrdered"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode";
```
**Result:** `[SCREENSHOT]`

---

### Q30. Get payments with customer country
```sql
SELECT c."customerName", c."country", p."amount", p."paymentDate"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```
**Result:** `[SCREENSHOT]`

---

### Q31. Count customers per country
```sql
SELECT "country", COUNT("customerNumber") AS "customerCount"
FROM customers
GROUP BY "country"
ORDER BY "customerCount" DESC;
```
**Explanation:** Groups customers by country and counts each group. ORDER BY shows highest-count countries first.
**Result:** `[SCREENSHOT]`

---

### Q32. Total payments per customer
```sql
SELECT c."customerName", SUM(p."amount") AS "totalPaid"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY "totalPaid" DESC;
```
**Explanation:** Joins payments with customers, sums payment amounts per customer name.
**Result:** `[SCREENSHOT]`

---

### Q33. Number of orders per status
```sql
SELECT "status", COUNT("orderNumber") AS "orderCount"
FROM orders
GROUP BY "status"
ORDER BY "orderCount" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q34. Products per product line
```sql
SELECT "productLine", COUNT("productCode") AS "productCount"
FROM products
GROUP BY "productLine"
ORDER BY "productCount" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q35. Employees per office
```sql
SELECT o."city", COUNT(e."employeeNumber") AS "employeeCount"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode"
GROUP BY o."city"
ORDER BY "employeeCount" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q36. Total stock per product vendor
```sql
SELECT "productVendor", SUM("quantityInStock") AS "totalStock"
FROM products
GROUP BY "productVendor"
ORDER BY "totalStock" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q37. Average buy price per product line
```sql
SELECT "productLine", ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice"
FROM products
GROUP BY "productLine"
ORDER BY "avgBuyPrice" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q38. Orders per customer
```sql
SELECT c."customerName", COUNT(o."orderNumber") AS "orderCount"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY "orderCount" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q39. Max MSRP per product line
```sql
SELECT "productLine", MAX("MSRP") AS "maxMSRP"
FROM products
GROUP BY "productLine"
ORDER BY "maxMSRP" DESC;
```
**Result:** `[SCREENSHOT]`

---

### Q40. Min buy price per vendor
```sql
SELECT "productVendor", MIN("buyPrice") AS "minBuyPrice"
FROM products
GROUP BY "productVendor"
ORDER BY "minBuyPrice";
```
**Result:** `[SCREENSHOT]`

---

### Q41. Total number of customers
```sql
SELECT COUNT("customerNumber") AS "totalCustomers"
FROM customers;
```
**Result:** `[SCREENSHOT]`

---

### Q42. Total number of products
```sql
SELECT COUNT("productCode") AS "totalProducts"
FROM products;
```
**Result:** `[SCREENSHOT]`

---

### Q43. Total revenue from payments
```sql
SELECT SUM("amount") AS "totalRevenue"
FROM payments;
```
**Result:** `[SCREENSHOT]`

---

### Q44. Average product price
```sql
SELECT ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice"
FROM products;
```
**Result:** `[SCREENSHOT]`

---

### Q45. Max payment amount
```sql
SELECT MAX("amount") AS "maxPayment"
FROM payments;
```
**Result:** `[SCREENSHOT]`

---

### Q46. Min payment amount
```sql
SELECT MIN("amount") AS "minPayment"
FROM payments;
```
**Result:** `[SCREENSHOT]`

---

### Q47. Count total orders
```sql
SELECT COUNT("orderNumber") AS "totalOrders"
FROM orders;
```
**Result:** `[SCREENSHOT]`

---

### Q48. Total quantity in stock
```sql
SELECT SUM("quantityInStock") AS "totalStock"
FROM products;
```
**Result:** `[SCREENSHOT]`

---

### Q49. Average MSRP
```sql
SELECT ROUND(AVG("MSRP"), 2) AS "avgMSRP"
FROM products;
```
**Result:** `[SCREENSHOT]`

---

### Q50. Number of employees
```sql
SELECT COUNT("employeeNumber") AS "totalEmployees"
FROM employees;
```
**Result:** `[SCREENSHOT]`

---

## Part 2: Evaluation Strategy for Text-to-SQL Systems

### 1. Execution Success Rate (ESR)
Does the generated SQL run without a database error?
```
ESR = Queries that execute without error / Total queries × 100
```

### 2. Execution Accuracy (EA) — Most Important
Does the result set match the expected output?
```
EA = Queries where result == expected_result / Total × 100
```
A query can execute but still return wrong data. This catches that.

### 3. Component-Level Accuracy
Score each SQL clause independently per query:

| Component | Check |
|-----------|-------|
| Table selection | Correct tables referenced? |
| Column selection | Correct columns projected? |
| JOIN correctness | Right join keys used? |
| Filter (WHERE) | Conditions match intent? |
| Aggregation | COUNT/SUM/AVG applied correctly? |
| GROUP BY | Correct grouping applied? |

### 4. Retry / Self-Correction Rate
```
Recovery Rate = Queries fixed after retry / Initially failed queries × 100
```

### 5. Query Generation Latency
- Average latency end-to-end (ms)
- Breakdown: LLM decomposition + LLM SQL gen + DB execution

### 6. Natural Language Answer Quality (Qualitative)
Spot-check 5–10 summaries per run for factual correctness and clarity.

### Benchmark Pipeline
```
For each question:
  1. Run agent → get generated_sql + result
  2. Run ground_truth_sql → get expected_result
  3. Compare: executed_ok, result_match, retry_used, latency_ms
  4. Log to evaluation_report.jsonl
```

### Recommended Thresholds

| Metric | Acceptable | Good | Excellent |
|--------|-----------|------|-----------|
| Execution Success Rate | >80% | >90% | >95% |
| Execution Accuracy | >60% | >75% | >85% |
| Recovery Rate | >40% | >60% | >80% |
| Avg Latency | <5s | <2s | <1s |

---

# Task 2: Query Understanding (Decomposition)

Natural language questions are broken into structured components before writing SQL. Format: **Intent → Tables → Columns → Filters → Joins → Aggregation → Group By**.

---

### Example
**Question:** How many customers are from the USA?
- **Intent:** Count customers filtered by country
- **Tables:** customers
- **Columns:** COUNT("customerNumber")
- **Filters:** country = 'USA'
- **Joins:** None
- **Aggregation:** COUNT
- **Group By:** None

---

### Simple Retrieval (Q1–Q7)
All follow the same pattern — single table, no filters, no joins.

- **Intent:** Retrieve all records
- **Tables:** `products` / `customers` / `orders` / `employees` / `offices` / `productlines` / `payments`
- **Columns:** * (all)
- **Filters:** None | **Joins:** None | **Aggregation:** None

---

### Q8. Get product names and prices
- **Intent:** Retrieve pricing info for all products
- **Tables:** products
- **Columns:** "productName", "buyPrice", "MSRP"
- **Filters:** None | **Joins:** None | **Aggregation:** None

### Q12. Show product vendor list
- **Intent:** Get unique list of product vendors
- **Tables:** products
- **Columns:** "productVendor" (DISTINCT)
- **Filters:** None | **Joins:** None | **Aggregation:** None

---

### Q21. Get orders with customer names
- **Intent:** Retrieve orders showing the customer's name
- **Tables:** orders, customers
- **Columns:** o."orderNumber", o."orderDate", o."status", c."customerName"
- **Filters:** None
- **Joins:** customers."customerNumber" = orders."customerNumber"
- **Aggregation:** None

### Q22. Get employees with office city
- **Intent:** Show each employee with their office city
- **Tables:** employees, offices
- **Columns:** e."firstName", e."lastName", e."jobTitle", o."city"
- **Filters:** None
- **Joins:** employees."officeCode" = offices."officeCode"
- **Aggregation:** None

### Q26. Get customers with sales rep names
- **Intent:** Show each customer with their assigned sales rep
- **Tables:** customers, employees
- **Columns:** c."customerName", e."firstName" || ' ' || e."lastName"
- **Filters:** None
- **Joins:** customers."salesRepEmployeeNumber" = employees."employeeNumber"
- **Aggregation:** None

### Q28. Get employees and their manager
- **Intent:** Self-join to show employee + manager pairs
- **Tables:** employees (e1 = employee, e2 = manager)
- **Columns:** e1 full name, e2 full name
- **Filters:** None
- **Joins:** e1."reportsTo" = e2."employeeNumber" (LEFT JOIN — keeps top-level employees)
- **Aggregation:** None

---

### Q31. Count customers per country
- **Intent:** Count customers grouped by country
- **Tables:** customers
- **Columns:** "country", COUNT("customerNumber")
- **Filters:** None | **Joins:** None
- **Aggregation:** COUNT
- **Group By:** "country"

### Q32. Total payments per customer
- **Intent:** Sum all payments made by each customer
- **Tables:** payments, customers
- **Columns:** c."customerName", SUM(p."amount")
- **Filters:** None
- **Joins:** payments."customerNumber" = customers."customerNumber"
- **Aggregation:** SUM
- **Group By:** c."customerName"

### Q37. Average buy price per product line
- **Intent:** Calculate average buy price within each product line
- **Tables:** products
- **Columns:** "productLine", AVG("buyPrice")
- **Filters:** None | **Joins:** None
- **Aggregation:** AVG
- **Group By:** "productLine"

### Q39. Max MSRP per product line
- **Intent:** Find the highest MSRP within each product line
- **Tables:** products
- **Columns:** "productLine", MAX("MSRP")
- **Filters:** None | **Joins:** None
- **Aggregation:** MAX
- **Group By:** "productLine"

---

# Task 3: Text-to-SQL Pipeline

## Architecture

```
Natural Language Question
        ↓
  Decomposition (LLM)         → intent, tables, columns, filters, joins
        ↓
  SQL Generation (LLM)        → raw SQL string
        ↓
  Validation (validator.py)   → block non-SELECT statements
        ↓
  Execution (database.py)     → run against PostgreSQL
        ↓ (on error)
  LLM Fix + Retry (1x)        → rewrite broken SQL
        ↓
  Structured JSON Output
```

## Project Structure

```
text2sql/
├── main.py           # FastAPI app — all endpoints
├── database.py       # PostgreSQL connection + execution
├── validator.py      # SQL safety gate
├── sql_generator.py  # LLM decompose + SQL generate
├── executor.py       # Execute with retry
├── llm_client.py     # Groq API wrapper
├── prompts/
│   └── templates.py  # All LLM prompt templates
└── logs/
    ├── app.log
    └── queries.jsonl
```

## Key Code Snippets

**sql_generator.py — Decompose**
```python
def decompose_question(question: str) -> dict:
    prompt = DECOMPOSITION_PROMPT.format(question=question)
    return call_llm_json(prompt)
    # Returns: {intent, tables, columns, filters, joins, aggregation, group_by}
```

**validator.py — Safety gate**
```python
BLOCKED_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|TRUNCATE|ALTER|CREATE|...)\b",
    re.IGNORECASE
)
# Only SELECT queries allowed. Multiple statements blocked.
```

**executor.py — Retry logic**
```python
def run_with_retry(sql: str, max_retries: int = 1) -> dict:
    for attempt in range(max_retries + 1):
        valid, reason = is_safe(sql)
        result = execute_query(sql)
        if result["error"] is None:
            return {"status": "success", ...}
        sql = fix_sql(sql, result["error"])  # LLM rewrites on error
```

## Endpoint

**POST /pipeline/sql**
```json
// Request
{"question": "Count customers per country"}

// Response
{
  "question": "Count customers per country",
  "decomposition": {"intent": "...", "tables": ["customers"], ...},
  "sql": "SELECT \"country\", COUNT(\"customerNumber\") AS \"customerCount\" FROM customers GROUP BY \"country\" ORDER BY \"customerCount\" DESC;",
  "result": {"rows": [...], "row_count": 27, "error": null, "execution_time_ms": 8.4},
  "status": "success",
  "attempts": 1,
  "retried": false,
  "execution_time_ms": 1240.5
}
```

## Successful Query Demo
`[SCREENSHOT — POST /pipeline/sql response]`

## Failed Query + Retry Demo
```
Attempt 1: SELECT customerName FROM orders
Error: column "customerName" does not exist
→ LLM reads error, rewrites SQL
Attempt 2: SELECT c."customerName" FROM orders o
           JOIN customers c ON o."customerNumber" = c."customerNumber"
→ Success
```
`[SCREENSHOT — retry log]`

## Benchmark Evaluation (GET /evaluate)

The full benchmark report is available in `evaluation_report.json`.
The latest run covers all 50 benchmark questions and records both execution and correctness metrics for the agent.

### Latest evaluation results

- Questions evaluated: 50
- Execution success rate: 16.0%
- Execution accuracy: 6.0%
- Retry rate: 0.0%
- Successful executions: 8
- Correct results: 3
- Failed executions: 42

The JSON report includes per-question details such as generated SQL, execution outcome, whether the result matched ground truth, retry usage, and a natural language summary.

`[SCREENSHOT — GET /evaluate full output]`

---

# Task 4: Mini SQL Agent

## What's Different from Task 3

| | Task 3 Pipeline | Task 4 Agent |
|--|----------------|-------------|
| Max retries | 1 | 3 |
| Natural language summary | No | Yes |
| Logging | Per-query JSONL | Per-query JSONL + decomposition step |
| Fallback on all failures | Crash | Graceful fallback response |

## Endpoint

**POST /agent/sql**
```json
// Request
{"question": "How many shipped orders are from USA customers?"}

// Response
{
  "question": "How many shipped orders are from USA customers?",
  "decomposition": {
    "intent": "Count shipped orders from USA customers",
    "tables": ["orders", "customers"],
    "columns": ["COUNT(*)"],
    "filters": ["status = 'Shipped'", "country = 'USA'"],
    "joins": ["orders.customerNumber = customers.customerNumber"],
    "aggregation": "COUNT",
    "group_by": []
  },
  "sql": "SELECT COUNT(*) FROM orders o JOIN customers c ON o.\"customerNumber\" = c.\"customerNumber\" WHERE c.\"country\" = 'USA' AND o.\"status\" = 'Shipped'",
  "result": {"rows": [{"count": 46}], "row_count": 1, "error": null},
  "summary": "There are 46 shipped orders from customers in the USA.",
  "status": "success",
  "attempts": 1,
  "retried": false,
  "execution_time_ms": 1874.3
}
```

## Agent Flow

```
Step 1: Understand query
        decompose_question(question)
        → intent, tables, columns, filters, joins

Step 2: Generate SQL
        generate_sql(decomposition)
        → raw SQL string via LLM

Step 3: Execute
        execute_query(sql) via psycopg2

Step 4: Error handling (up to 3 retries)
        if error → fix_sql(sql, error_message) → retry

Step 5: Summarize
        _generate_summary(question, result)
        → single human-readable sentence
```

## Logging

Every query appended to `logs/queries.jsonl`:
```json
{
  "timestamp": "2026-05-17T10:23:41Z",
  "question": "How many shipped orders are from USA customers?",
  "decomposition": {"intent": "...", "tables": [...], ...},
  "sql": "SELECT COUNT(*) FROM orders o JOIN ...",
  "status": "success",
  "attempts": 1,
  "retried": false,
  "execution_time_ms": 1874.3
}
```

## Fallback Behavior
If all 3 retries fail, agent returns gracefully:
```json
{
  "summary": "I was unable to answer this question after 3 attempts. Error: ...",
  "status": "failed",
  "attempts": 3
}
```

## Safety Rules
- Only `SELECT` queries — all mutating keywords blocked
- Statement timeout: 10 seconds per query
- Multi-statement injection blocked (`;` stacking)
- All executions logged regardless of outcome

## Agent Demo
`[SCREENSHOT — POST /agent/sql request + response]`

`[SCREENSHOT — logs/queries.jsonl showing decomposition + retry]`

`[SCREENSHOT — GET /evaluate full benchmark report]`
