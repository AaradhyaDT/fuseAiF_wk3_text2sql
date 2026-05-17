"""
Generate Task 1 Part 1 document with all 50 ground truth SQL queries and results.
"""

import psycopg
import json
import os
from datetime import datetime

# Database config
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "classicmodels"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "password"),
}

# All 50 benchmark questions with SQL
BENCHMARK_QUERIES = [
    # Simple SELECT (Q1–Q20)
    ("Q1. List all products", 'SELECT * FROM products;'),
    ("Q2. Get all customers", 'SELECT * FROM customers;'),
    ("Q3. Show all orders", 'SELECT * FROM orders;'),
    ("Q4. List all employees", 'SELECT * FROM employees;'),
    ("Q5. Get all offices", 'SELECT * FROM offices;'),
    ("Q6. Show all product lines", 'SELECT * FROM productlines;'),
    ("Q7. List all payments", 'SELECT * FROM payments;'),
    ("Q8. Get product names and prices", 'SELECT "productName", "buyPrice", "MSRP" FROM products;'),
    ("Q9. Get customer names and cities", 'SELECT "customerName", city FROM customers;'),
    ("Q10. List employee first and last names", 'SELECT "firstName", "lastName" FROM employees;'),
    ("Q11. Get all order dates", 'SELECT "orderNumber", "orderDate" FROM orders;'),
    ("Q12. Show product vendor list", 'SELECT DISTINCT "productVendor" FROM products;'),
    ("Q13. Get all product codes", 'SELECT "productCode" FROM products;'),
    ("Q14. List all countries from offices", 'SELECT DISTINCT country FROM offices;'),
    ("Q15. Show all order statuses", 'SELECT DISTINCT status FROM orders;'),
    ("Q16. Get all payment amounts", 'SELECT "checkNumber", amount, "paymentDate" FROM payments;'),
    ("Q17. List all job titles", 'SELECT DISTINCT "jobTitle" FROM employees;'),
    ("Q18. Get customer phone numbers", 'SELECT "customerName", phone FROM customers;'),
    ("Q19. Show product MSRP values", 'SELECT "productName", "MSRP" FROM products;'),
    ("Q20. List order numbers", 'SELECT "orderNumber" FROM orders;'),
    
    # JOIN Queries (Q21–Q30)
    ("Q21. Get orders with customer names", 'SELECT o."orderNumber", o."orderDate", c."customerName" FROM orders o JOIN customers c ON o."customerNumber" = c."customerNumber";'),
    ("Q22. Get employees with office city", 'SELECT e."firstName", e."lastName", of.city FROM employees e JOIN offices of ON e."officeCode" = of."officeCode";'),
    ("Q23. Get payments with customer names", 'SELECT c."customerName", p."checkNumber", p.amount, p."paymentDate" FROM payments p JOIN customers c ON p."customerNumber" = c."customerNumber";'),
    ("Q24. Get order details with product names", 'SELECT od."orderNumber", pr."productName", od."quantityOrdered", od."priceEach" FROM orderdetails od JOIN products pr ON od."productCode" = pr."productCode";'),
    ("Q25. Get products with product line description", 'SELECT pr."productName", pl."textDescription" FROM products pr JOIN productlines pl ON pr."productLine" = pl."productLine";'),
    ("Q26. Get customers with sales rep names", 'SELECT c."customerName", e."firstName" || \' \' || e."lastName" AS "salesRepName" FROM customers c JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber";'),
    ("Q27. Get orders with customer city", 'SELECT o."orderNumber", o."orderDate", c.city FROM orders o JOIN customers c ON o."customerNumber" = c."customerNumber";'),
    ("Q28. Get employees and their manager", 'SELECT e."firstName" || \' \' || e."lastName" AS employee, m."firstName" || \' \' || m."lastName" AS manager FROM employees e LEFT JOIN employees m ON e."reportsTo" = m."employeeNumber";'),
    ("Q29. Get order details with product vendor", 'SELECT od."orderNumber", pr."productVendor", od."quantityOrdered" FROM orderdetails od JOIN products pr ON od."productCode" = pr."productCode";'),
    ("Q30. Get payments with customer country", 'SELECT p."checkNumber", p.amount, c.country FROM payments p JOIN customers c ON p."customerNumber" = c."customerNumber";'),
    
    # Aggregation Queries (Q31–Q40)
    ("Q31. Count customers per country", 'SELECT country, COUNT("customerNumber") AS customer_count FROM customers GROUP BY country ORDER BY customer_count DESC;'),
    ("Q32. Total payments per customer", 'SELECT c."customerName", SUM(p.amount) AS total_paid FROM payments p JOIN customers c ON p."customerNumber" = c."customerNumber" GROUP BY c."customerName" ORDER BY total_paid DESC;'),
    ("Q33. Number of orders per status", 'SELECT status, COUNT("orderNumber") AS order_count FROM orders GROUP BY status;'),
    ("Q34. Products per product line", 'SELECT "productLine", COUNT("productCode") AS product_count FROM products GROUP BY "productLine" ORDER BY product_count DESC;'),
    ("Q35. Employees per office", 'SELECT of.city, COUNT(e."employeeNumber") AS employee_count FROM employees e JOIN offices of ON e."officeCode" = of."officeCode" GROUP BY of.city ORDER BY employee_count DESC;'),
    ("Q36. Total stock per product vendor", 'SELECT "productVendor", SUM("quantityInStock") AS total_stock FROM products GROUP BY "productVendor" ORDER BY total_stock DESC;'),
    ("Q37. Average buy price per product line", 'SELECT "productLine", ROUND(AVG("buyPrice"), 2) AS avg_buy_price FROM products GROUP BY "productLine" ORDER BY avg_buy_price DESC;'),
    ("Q38. Orders per customer", 'SELECT c."customerName", COUNT(o."orderNumber") AS order_count FROM orders o JOIN customers c ON o."customerNumber" = c."customerNumber" GROUP BY c."customerName" ORDER BY order_count DESC;'),
    ("Q39. Max MSRP per product line", 'SELECT "productLine", MAX("MSRP") AS max_msrp FROM products GROUP BY "productLine";'),
    ("Q40. Min buy price per vendor", 'SELECT "productVendor", MIN("buyPrice") AS min_buy_price FROM products GROUP BY "productVendor";'),
    
    # Single-Value Aggregate Queries (Q41–Q50)
    ("Q41. Total number of customers", 'SELECT COUNT("customerNumber") AS total_customers FROM customers;'),
    ("Q42. Total number of products", 'SELECT COUNT("productCode") AS total_products FROM products;'),
    ("Q43. Total revenue from payments", 'SELECT SUM(amount) AS total_revenue FROM payments;'),
    ("Q44. Average product price", 'SELECT ROUND(AVG("buyPrice"), 2) AS avg_buy_price FROM products;'),
    ("Q45. Max payment amount", 'SELECT MAX(amount) AS max_payment FROM payments;'),
    ("Q46. Min payment amount", 'SELECT MIN(amount) AS min_payment FROM payments;'),
    ("Q47. Count total orders", 'SELECT COUNT("orderNumber") AS total_orders FROM orders;'),
    ("Q48. Total quantity in stock", 'SELECT SUM("quantityInStock") AS total_stock FROM products;'),
    ("Q49. Average MSRP", 'SELECT ROUND(AVG("MSRP"), 2) AS avg_msrp FROM products;'),
    ("Q50. Number of employees", 'SELECT COUNT("employeeNumber") AS total_employees FROM employees;'),
]


def run_query(conn, sql):
    """Execute a query and return results."""
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows = cur.fetchall()
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                return {
                    "success": True,
                    "columns": columns,
                    "rows": rows,
                    "row_count": len(rows),
                    "error": None
                }
            return {
                "success": True,
                "columns": [],
                "rows": [],
                "row_count": 0,
                "error": None
            }
    except Exception as e:
        return {
            "success": False,
            "columns": [],
            "rows": [],
            "row_count": 0,
            "error": str(e)
        }


def format_value(val):
    """Format a value for display."""
    if val is None:
        return "NULL"
    elif isinstance(val, (int, float)):
        return str(val)
    elif isinstance(val, str):
        return val[:50] + "..." if len(val) > 50 else val
    else:
        return str(val)


def generate_markdown_doc(results):
    """Generate markdown document with all results."""
    doc = """# Task 1 — Part 1: Ground Truth SQL Queries and Results

**Date Generated:** """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """

## Overview

This document contains all 50 benchmark questions from the FUSE AI Fellowship Week 3 assignment, along with their ground-truth SQL queries and expected results. These queries have been executed against the classicmodels PostgreSQL database to establish the baseline for evaluating Text-to-SQL systems.

---

## Query Results

"""
    
    for question, sql in BENCHMARK_QUERIES:
        qnum = question.split(".")[0]
        doc += f"\n### {question}\n\n"
        doc += f"**SQL Query:**\n```sql\n{sql}\n```\n\n"
        
        if question in results:
            result = results[question]
            if result["success"]:
                doc += f"**Execution Status:** SUCCESS\n\n"
                doc += f"**Row Count:** {result['row_count']}\n\n"
                
                if result['rows']:
                    doc += "**Results:**\n\n"
                    # Show first 10 rows in table format
                    if result['columns']:
                        doc += "| " + " | ".join(result['columns'][:5]) + (" | ..." if len(result['columns']) > 5 else "") + " |\n"
                        doc += "| " + " | ".join(["---"] * min(5, len(result['columns']))) + (" | ---" if len(result['columns']) > 5 else "") + " |\n"
                        
                        for row in result['rows'][:10]:
                            values = [format_value(v) for v in row[:5]]
                            doc += "| " + " | ".join(values) + (" | ..." if len(result['columns']) > 5 else "") + " |\n"
                        
                        if result['row_count'] > 10:
                            doc += f"\n*(Showing first 10 of {result['row_count']} rows)*\n"
                else:
                    doc += "**Results:** No rows returned\n\n"
            else:
                doc += f"**Execution Status:** FAILED\n\n"
                doc += f"**Error:** {result['error']}\n\n"
        
        doc += "\n---\n"
    
    doc += """

## Evaluation Notes

### Simple SELECT Queries (Q1–Q20)
These queries test basic table retrieval and column selection capabilities. They are fundamental operations that any Text-to-SQL system must handle correctly.

### JOIN Queries (Q21–Q30)
These queries require proper identification of table relationships and join conditions. Q28 specifically tests self-joins and the use of LEFT JOIN for handling missing references.

### Aggregation Queries (Q31–Q40)
These queries test GROUP BY, COUNT, SUM, AVG, MAX, MIN operations. They require the system to understand which columns can be aggregated and how to properly group results.

### Single-Value Aggregate Queries (Q41–Q50)
These queries return single scalar values. They test the system's ability to apply aggregate functions without grouping.

---

## Key Schema Reminders

All column names in the classicmodels database use camelCase and **must be double-quoted in SQL**:

- `"productCode"`, `"productName"`, `"productLine"`
- `"customerNumber"`, `"customerName"`, `"salesRepEmployeeNumber"`
- `"employeeNumber"`, `"firstName"`, `"lastName"`, `"jobTitle"`, `"officeCode"`, `"reportsTo"`
- `"orderNumber"`, `"orderDate"`, `"status"`, `"quantityInStock"`
- `"checkNumber"`, `"paymentDate"`, `"quantityOrdered"`, `"priceEach"`, `"buyPrice"`, `"MSRP"`

---

"""
    
    return doc


def main():
    try:
        print("Connecting to database...")
        conn = psycopg.connect(**DB_CONFIG)
        print(f"Connected to {DB_CONFIG['dbname']} @ {DB_CONFIG['host']}")
        
        results = {}
        successful = 0
        failed = 0
        
        print("\nExecuting all 50 queries...")
        for i, (question, sql) in enumerate(BENCHMARK_QUERIES, 1):
            result = run_query(conn, sql)
            results[question] = result
            
            if result["success"]:
                successful += 1
                print(f"[{i:2d}/50] OK {question.split('.')[0]}")
            else:
                failed += 1
                print(f"[{i:2d}/50] FAIL {question.split('.')[0]} - {result['error']}")
        
        conn.close()
        
        print(f"\nOK {successful} queries succeeded, FAIL {failed} queries failed")
        
        # Generate markdown document
        print("\nGenerating Task1_Part1_Ground_Truth.md...")
        doc = generate_markdown_doc(results)
        
        with open("Task1_Part1_Ground_Truth.md", "w", encoding="utf-8") as f:
            f.write(doc)
        
        print("[OK] Document saved to Task1_Part1_Ground_Truth.md")
        
        # Save results as JSON
        json_results = {}
        for question, result in results.items():
            json_results[question] = {
                "sql": [q for q, _ in BENCHMARK_QUERIES if q == question][0] if question in [q for q, _ in BENCHMARK_QUERIES] else "",
                "success": result["success"],
                "row_count": result["row_count"],
                "columns": result["columns"],
                "error": result["error"]
            }
        
        with open("task1_ground_truth_results.json", "w", encoding="utf-8") as f:
            json.dump(json_results, f, indent=2, default=str)
        
        print("✓ Results saved to task1_ground_truth_results.json")
        
    except Exception as e:
        print(f"FAIL Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
