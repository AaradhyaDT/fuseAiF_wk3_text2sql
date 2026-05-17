# Task 2 — Query Understanding: Full Decomposition

All 50 benchmark questions decomposed into structured components.

Format per question:
- **Intent**
- **Tables**
- **Columns**
- **Filters**
- **Joins**
- **Aggregation / GROUP BY**

---

## Simple Retrieval (Q1–Q20)

---

### Q1. List all products
- **Intent:** Retrieve all product records
- **Tables:** products
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM products;
```

---

### Q2. Get all customers
- **Intent:** Retrieve all customer records
- **Tables:** customers
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM customers;
```

---

### Q3. Show all orders
- **Intent:** Retrieve all order records
- **Tables:** orders
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM orders;
```

---

### Q4. List all employees
- **Intent:** Retrieve all employee records
- **Tables:** employees
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM employees;
```

---

### Q5. Get all offices
- **Intent:** Retrieve all office records
- **Tables:** offices
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM offices;
```

---

### Q6. Show all product lines
- **Intent:** Retrieve all product line records
- **Tables:** productlines
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM productlines;
```

---

### Q7. List all payments
- **Intent:** Retrieve all payment records
- **Tables:** payments
- **Columns:** * (all)
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT * FROM payments;
```

---

### Q8. Get product names and prices
- **Intent:** Retrieve product names alongside their buy price and MSRP
- **Tables:** products
- **Columns:** "productName", "buyPrice", "MSRP"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "productName", "buyPrice", "MSRP"
FROM products;
```

---

### Q9. Get customer names and cities
- **Intent:** Retrieve customer name and city for all customers
- **Tables:** customers
- **Columns:** "customerName", "city"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "customerName", "city"
FROM customers;
```

---

### Q10. List employee first and last names
- **Intent:** Retrieve employee full names
- **Tables:** employees
- **Columns:** "firstName", "lastName"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "firstName", "lastName"
FROM employees;
```

---

### Q11. Get all order dates
- **Intent:** Retrieve order dates
- **Tables:** orders
- **Columns:** "orderNumber", "orderDate"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "orderNumber", "orderDate"
FROM orders;
```

---

### Q12. Show product vendor list
- **Intent:** Retrieve distinct product vendors
- **Tables:** products
- **Columns:** "productVendor"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT DISTINCT "productVendor"
FROM products;
```

---

### Q13. Get all product codes
- **Intent:** Retrieve all product codes
- **Tables:** products
- **Columns:** "productCode"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "productCode"
FROM products;
```

---

### Q14. List all countries from offices
- **Intent:** Retrieve distinct countries where offices are located
- **Tables:** offices
- **Columns:** "country"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT DISTINCT "country"
FROM offices;
```

---

### Q15. Show all order statuses
- **Intent:** Retrieve distinct order statuses
- **Tables:** orders
- **Columns:** "status"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT DISTINCT "status"
FROM orders;
```

---

### Q16. Get all payment amounts
- **Intent:** Retrieve all payment amounts
- **Tables:** payments
- **Columns:** "customerNumber", "checkNumber", "amount"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "customerNumber", "checkNumber", "amount"
FROM payments;
```

---

### Q17. List all job titles
- **Intent:** Retrieve distinct job titles from employees
- **Tables:** employees
- **Columns:** "jobTitle"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT DISTINCT "jobTitle"
FROM employees;
```

---

### Q18. Get customer phone numbers
- **Intent:** Retrieve customer names and phone numbers
- **Tables:** customers
- **Columns:** "customerName", "phone"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "customerName", "phone"
FROM customers;
```

---

### Q19. Show product MSRP values
- **Intent:** Retrieve product names with their MSRP
- **Tables:** products
- **Columns:** "productName", "MSRP"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "productName", "MSRP"
FROM products;
```

---

### Q20. List order numbers
- **Intent:** Retrieve all order numbers
- **Tables:** orders
- **Columns:** "orderNumber"
- **Filters:** None
- **Joins:** None

**SQL:**
```sql
SELECT "orderNumber"
FROM orders;
```

---

## Join Queries (Q21–Q30)

---

### Q21. Get orders with customer names
- **Intent:** Retrieve orders showing the customer's name
- **Tables:** orders, customers
- **Columns:** o."orderNumber", o."orderDate", o."status", c."customerName"
- **Filters:** None
- **Joins:** customers."customerNumber" = orders."customerNumber"

**SQL:**
```sql
SELECT o."orderNumber", o."orderDate", o."status", c."customerName"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```

---

### Q22. Get employees with office city
- **Intent:** Show each employee alongside the city of their office
- **Tables:** employees, offices
- **Columns:** e."firstName", e."lastName", e."jobTitle", o."city"
- **Filters:** None
- **Joins:** employees."officeCode" = offices."officeCode"

**SQL:**
```sql
SELECT e."firstName", e."lastName", e."jobTitle", o."city"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode";
```

---

### Q23. Get payments with customer names
- **Intent:** Show payment records with the corresponding customer name
- **Tables:** payments, customers
- **Columns:** c."customerName", p."checkNumber", p."paymentDate", p."amount"
- **Filters:** None
- **Joins:** payments."customerNumber" = customers."customerNumber"

**SQL:**
```sql
SELECT c."customerName", p."checkNumber", p."paymentDate", p."amount"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```

---

### Q24. Get order details with product names
- **Intent:** Show order line items with product names
- **Tables:** orderdetails, products
- **Columns:** od."orderNumber", p."productName", od."quantityOrdered", od."priceEach"
- **Filters:** None
- **Joins:** orderdetails."productCode" = products."productCode"

**SQL:**
```sql
SELECT od."orderNumber", p."productName", od."quantityOrdered", od."priceEach"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode";
```

---

### Q25. Get products with product line description
- **Intent:** Show each product alongside its product line's text description
- **Tables:** products, productlines
- **Columns:** p."productName", pl."productLine", pl."textDescription"
- **Filters:** None
- **Joins:** products."productLine" = productlines."productLine"

**SQL:**
```sql
SELECT p."productName", pl."productLine", pl."textDescription"
FROM products p
JOIN productlines pl ON p."productLine" = pl."productLine";
```

---

### Q26. Get customers with sales rep names
- **Intent:** Show each customer with the name of their assigned sales rep
- **Tables:** customers, employees
- **Columns:** c."customerName", e."firstName", e."lastName"
- **Filters:** None
- **Joins:** customers."salesRepEmployeeNumber" = employees."employeeNumber"

**SQL:**
```sql
SELECT c."customerName",
       e."firstName" || ' ' || e."lastName" AS "salesRepName"
FROM customers c
JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber";
```

---

### Q27. Get orders with customer city
- **Intent:** Show orders alongside the city of the ordering customer
- **Tables:** orders, customers
- **Columns:** o."orderNumber", o."orderDate", c."customerName", c."city"
- **Filters:** None
- **Joins:** orders."customerNumber" = customers."customerNumber"

**SQL:**
```sql
SELECT o."orderNumber", o."orderDate", c."customerName", c."city"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber";
```

---

### Q28. Get employees and their manager
- **Intent:** Show each employee alongside their manager's name (self-join)
- **Tables:** employees (self-join: e1 = employee, e2 = manager)
- **Columns:** e1."firstName", e1."lastName", e2."firstName" AS manager
- **Filters:** None
- **Joins:** e1."reportsTo" = e2."employeeNumber"

**SQL:**
```sql
SELECT e1."firstName" || ' ' || e1."lastName" AS "employee",
       e2."firstName" || ' ' || e2."lastName" AS "manager"
FROM employees e1
LEFT JOIN employees e2 ON e1."reportsTo" = e2."employeeNumber";
```

---

### Q29. Get orderdetails with product vendor
- **Intent:** Show order line items with the vendor of each product
- **Tables:** orderdetails, products
- **Columns:** od."orderNumber", p."productName", p."productVendor", od."quantityOrdered"
- **Filters:** None
- **Joins:** orderdetails."productCode" = products."productCode"

**SQL:**
```sql
SELECT od."orderNumber", p."productName", p."productVendor", od."quantityOrdered"
FROM orderdetails od
JOIN products p ON od."productCode" = p."productCode";
```

---

### Q30. Get payments with customer country
- **Intent:** Show each payment alongside the customer's country
- **Tables:** payments, customers
- **Columns:** c."customerName", c."country", p."amount", p."paymentDate"
- **Filters:** None
- **Joins:** payments."customerNumber" = customers."customerNumber"

**SQL:**
```sql
SELECT c."customerName", c."country", p."amount", p."paymentDate"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber";
```

---

## Aggregation Queries (Q31–Q50)

---

### Q31. Count customers per country
- **Intent:** Count how many customers exist in each country
- **Tables:** customers
- **Columns:** "country", COUNT("customerNumber")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT
- **GROUP BY:** "country"

**SQL:**
```sql
SELECT "country", COUNT("customerNumber") AS "customerCount"
FROM customers
GROUP BY "country"
ORDER BY "customerCount" DESC;
```

---

### Q32. Total payments per customer
- **Intent:** Sum total payment amount per customer
- **Tables:** payments, customers
- **Columns:** c."customerName", SUM(p."amount")
- **Filters:** None
- **Joins:** payments."customerNumber" = customers."customerNumber"
- **Aggregation:** SUM
- **GROUP BY:** c."customerName"

**SQL:**
```sql
SELECT c."customerName", SUM(p."amount") AS "totalPaid"
FROM payments p
JOIN customers c ON p."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY "totalPaid" DESC;
```

---

### Q33. Number of orders per status
- **Intent:** Count orders grouped by status
- **Tables:** orders
- **Columns:** "status", COUNT("orderNumber")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT
- **GROUP BY:** "status"

**SQL:**
```sql
SELECT "status", COUNT("orderNumber") AS "orderCount"
FROM orders
GROUP BY "status"
ORDER BY "orderCount" DESC;
```

---

### Q34. Products per product line
- **Intent:** Count number of products in each product line
- **Tables:** products
- **Columns:** "productLine", COUNT("productCode")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT
- **GROUP BY:** "productLine"

**SQL:**
```sql
SELECT "productLine", COUNT("productCode") AS "productCount"
FROM products
GROUP BY "productLine"
ORDER BY "productCount" DESC;
```

---

### Q35. Employees per office
- **Intent:** Count employees at each office
- **Tables:** employees, offices
- **Columns:** o."city", COUNT(e."employeeNumber")
- **Filters:** None
- **Joins:** employees."officeCode" = offices."officeCode"
- **Aggregation:** COUNT
- **GROUP BY:** o."city"

**SQL:**
```sql
SELECT o."city", COUNT(e."employeeNumber") AS "employeeCount"
FROM employees e
JOIN offices o ON e."officeCode" = o."officeCode"
GROUP BY o."city"
ORDER BY "employeeCount" DESC;
```

---

### Q36. Total stock per product vendor
- **Intent:** Sum quantity in stock grouped by vendor
- **Tables:** products
- **Columns:** "productVendor", SUM("quantityInStock")
- **Filters:** None
- **Joins:** None
- **Aggregation:** SUM
- **GROUP BY:** "productVendor"

**SQL:**
```sql
SELECT "productVendor", SUM("quantityInStock") AS "totalStock"
FROM products
GROUP BY "productVendor"
ORDER BY "totalStock" DESC;
```

---

### Q37. Average buy price per product line
- **Intent:** Calculate average buy price for products in each product line
- **Tables:** products
- **Columns:** "productLine", AVG("buyPrice")
- **Filters:** None
- **Joins:** None
- **Aggregation:** AVG
- **GROUP BY:** "productLine"

**SQL:**
```sql
SELECT "productLine", ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice"
FROM products
GROUP BY "productLine"
ORDER BY "avgBuyPrice" DESC;
```

---

### Q38. Orders per customer
- **Intent:** Count total orders placed by each customer
- **Tables:** orders, customers
- **Columns:** c."customerName", COUNT(o."orderNumber")
- **Filters:** None
- **Joins:** orders."customerNumber" = customers."customerNumber"
- **Aggregation:** COUNT
- **GROUP BY:** c."customerName"

**SQL:**
```sql
SELECT c."customerName", COUNT(o."orderNumber") AS "orderCount"
FROM orders o
JOIN customers c ON o."customerNumber" = c."customerNumber"
GROUP BY c."customerName"
ORDER BY "orderCount" DESC;
```

---

### Q39. Max MSRP per product line
- **Intent:** Find the highest MSRP within each product line
- **Tables:** products
- **Columns:** "productLine", MAX("MSRP")
- **Filters:** None
- **Joins:** None
- **Aggregation:** MAX
- **GROUP BY:** "productLine"

**SQL:**
```sql
SELECT "productLine", MAX("MSRP") AS "maxMSRP"
FROM products
GROUP BY "productLine"
ORDER BY "maxMSRP" DESC;
```

---

### Q40. Min buy price per vendor
- **Intent:** Find the lowest buy price within each vendor's product range
- **Tables:** products
- **Columns:** "productVendor", MIN("buyPrice")
- **Filters:** None
- **Joins:** None
- **Aggregation:** MIN
- **GROUP BY:** "productVendor"

**SQL:**
```sql
SELECT "productVendor", MIN("buyPrice") AS "minBuyPrice"
FROM products
GROUP BY "productVendor"
ORDER BY "minBuyPrice";
```

---

### Q41. Total number of customers
- **Intent:** Count all customers
- **Tables:** customers
- **Columns:** COUNT("customerNumber")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT

**SQL:**
```sql
SELECT COUNT("customerNumber") AS "totalCustomers"
FROM customers;
```

---

### Q42. Total number of products
- **Intent:** Count all products
- **Tables:** products
- **Columns:** COUNT("productCode")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT

**SQL:**
```sql
SELECT COUNT("productCode") AS "totalProducts"
FROM products;
```

---

### Q43. Total revenue from payments
- **Intent:** Sum all payment amounts
- **Tables:** payments
- **Columns:** SUM("amount")
- **Filters:** None
- **Joins:** None
- **Aggregation:** SUM

**SQL:**
```sql
SELECT SUM("amount") AS "totalRevenue"
FROM payments;
```

---

### Q44. Average product price
- **Intent:** Calculate average buy price across all products
- **Tables:** products
- **Columns:** AVG("buyPrice")
- **Filters:** None
- **Joins:** None
- **Aggregation:** AVG

**SQL:**
```sql
SELECT ROUND(AVG("buyPrice"), 2) AS "avgBuyPrice"
FROM products;
```

---

### Q45. Max payment amount
- **Intent:** Find the largest single payment
- **Tables:** payments
- **Columns:** MAX("amount")
- **Filters:** None
- **Joins:** None
- **Aggregation:** MAX

**SQL:**
```sql
SELECT MAX("amount") AS "maxPayment"
FROM payments;
```

---

### Q46. Min payment amount
- **Intent:** Find the smallest single payment
- **Tables:** payments
- **Columns:** MIN("amount")
- **Filters:** None
- **Joins:** None
- **Aggregation:** MIN

**SQL:**
```sql
SELECT MIN("amount") AS "minPayment"
FROM payments;
```

---

### Q47. Count total orders
- **Intent:** Count all orders in the database
- **Tables:** orders
- **Columns:** COUNT("orderNumber")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT

**SQL:**
```sql
SELECT COUNT("orderNumber") AS "totalOrders"
FROM orders;
```

---

### Q48. Total quantity in stock
- **Intent:** Sum quantity in stock across all products
- **Tables:** products
- **Columns:** SUM("quantityInStock")
- **Filters:** None
- **Joins:** None
- **Aggregation:** SUM

**SQL:**
```sql
SELECT SUM("quantityInStock") AS "totalStock"
FROM products;
```

---

### Q49. Average MSRP
- **Intent:** Calculate average MSRP across all products
- **Tables:** products
- **Columns:** AVG("MSRP")
- **Filters:** None
- **Joins:** None
- **Aggregation:** AVG

**SQL:**
```sql
SELECT ROUND(AVG("MSRP"), 2) AS "avgMSRP"
FROM products;
```

---

### Q50. Number of employees
- **Intent:** Count all employees
- **Tables:** employees
- **Columns:** COUNT("employeeNumber")
- **Filters:** None
- **Joins:** None
- **Aggregation:** COUNT

**SQL:**
```sql
SELECT COUNT("employeeNumber") AS "totalEmployees"
FROM employees;
```
