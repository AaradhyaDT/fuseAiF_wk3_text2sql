"""
prompts/templates.py — Prompt templates for each pipeline stage
"""

# ── Full DB schema for context injection ────────────────────────────────────
SCHEMA_CONTEXT = """
PostgreSQL database schema (classicmodels):

Tables and columns:
- productlines(productLine PK, textDescription, htmlDescription, image)
- products(productCode PK, productName, productLine FK, productScale,
           productVendor, productDescription, quantityInStock,
           buyPrice NUMERIC, MSRP NUMERIC)
- offices(officeCode PK, city, phone, addressLine1, addressLine2,
          state, country, postalCode, territory)
- employees(employeeNumber PK, lastName, firstName, extension, email,
            officeCode FK→offices, reportsTo FK→employees, jobTitle)
- customers(customerNumber PK, customerName, contactLastName,
            contactFirstName, phone, addressLine1, addressLine2,
            city, state, postalCode, country,
            salesRepEmployeeNumber FK→employees, creditLimit NUMERIC)
- payments(customerNumber FK→customers, checkNumber, paymentDate DATE,
           amount NUMERIC)  [PK: customerNumber + checkNumber]
- orders(orderNumber PK, orderDate DATE, requiredDate DATE,
         shippedDate DATE, status, comments, customerNumber FK→customers)
- orderdetails(orderNumber FK→orders, productCode FK→products,
               quantityOrdered, priceEach NUMERIC, orderLineNumber)
  [PK: orderNumber + productCode]

Important notes:
- All column names are camelCase and MUST be quoted with double-quotes in SQL
  e.g. "customerNumber", "productLine", "orderDate"
- Table names are lowercase and do NOT need quoting
"""


DECOMPOSITION_PROMPT = """You are a SQL query analyst.

{schema}

Given the natural language question below, decompose it into structured components.
Respond ONLY with valid JSON — no markdown, no explanation, no backticks.

Question: {question}

Required JSON format:
{{
  "intent": "<what the query is doing>",
  "tables": ["<table1>", "<table2>"],
  "columns": ["<table.column or column>"],
  "filters": ["<condition1>", "<condition2>"],
  "joins": ["<table1.col = table2.col>"],
  "aggregation": "<COUNT/SUM/AVG/MAX/MIN or null>",
  "group_by": ["<column>"]
}}
"""


SQL_GENERATION_PROMPT = """You are a PostgreSQL expert.

{schema}

Given this structured decomposition, write a clean SQL SELECT query.
Respond ONLY with the raw SQL — no markdown, no explanation, no backticks.

Decomposition:
{decomposition}

Rules:
- ONLY SELECT queries
- Quote all camelCase column names with double-quotes
- Use table aliases
- Be correct and minimal
"""


SQL_FIX_PROMPT = """You are a PostgreSQL debugging expert.

{schema}

The following SQL query failed with this error:
Error: {error}

Original SQL:
{sql}

Rewrite the corrected SQL query.
Respond ONLY with the raw SQL — no markdown, no explanation, no backticks.
"""


SUMMARY_PROMPT = """You are a helpful data analyst.

Question: {question}

SQL Result (as JSON): {result}

Write a single clear sentence that directly answers the question using the data.
Be concise and factual. Do not mention SQL.
"""
