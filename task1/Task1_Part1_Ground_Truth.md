# Task 1 — Part 1: Ground Truth SQL Queries and Results

**Date Generated:** 2026-05-17 19:14:56

## Overview

This document contains all 50 benchmark questions from the FUSE AI Fellowship Week 3 assignment, along with their ground-truth SQL queries and expected results. These queries have been executed against the classicmodels PostgreSQL database to establish the baseline for evaluating Text-to-SQL systems.

---

## Query Results


### Q1. List all products

**SQL Query:**
```sql
SELECT * FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 110

**Results:**

| productCode | productName | productLine | productScale | productVendor | ... |
| --- | --- | --- | --- | --- | --- |
| S10_1678 | 1969 Harley Davidson Ultimate Chopper | Motorcycles | 1:10 | Min Lin Diecast | ... |
| S10_1949 | 1952 Alpine Renault 1300 | Classic Cars | 1:10 | Classic Metal Creations | ... |
| S10_2016 | 1996 Moto Guzzi 1100i | Motorcycles | 1:10 | Highway 66 Mini Classics | ... |
| S10_4698 | 2003 Harley-Davidson Eagle Drag Bike | Motorcycles | 1:10 | Red Start Diecast | ... |
| S10_4757 | 1972 Alfa Romeo GTA | Classic Cars | 1:10 | Motor City Art Classics | ... |
| S10_4962 | 1962 LanciaA Delta 16V | Classic Cars | 1:10 | Second Gear Diecast | ... |
| S12_1099 | 1968 Ford Mustang | Classic Cars | 1:12 | Autoart Studio Design | ... |
| S12_1108 | 2001 Ferrari Enzo | Classic Cars | 1:12 | Second Gear Diecast | ... |
| S12_1666 | 1958 Setra Bus | Trucks and Buses | 1:12 | Welly Diecast Productions | ... |
| S12_2823 | 2002 Suzuki XREO | Motorcycles | 1:12 | Unimax Art Galleries | ... |

*(Showing first 10 of 110 rows)*

---

### Q2. Get all customers

**SQL Query:**
```sql
SELECT * FROM customers;
```

**Execution Status:** SUCCESS

**Row Count:** 122

**Results:**

| customerNumber | customerName | contactLastName | contactFirstName | phone | ... |
| --- | --- | --- | --- | --- | --- |
| 103 | Atelier graphique | Schmitt | Carine  | 40.32.2555 | ... |
| 112 | Signal Gift Stores | King | Jean | 7025551838 | ... |
| 114 | Australian Collectors, Co. | Ferguson | Peter | 03 9520 4555 | ... |
| 119 | La Rochelle Gifts | Labrune | Janine  | 40.67.8555 | ... |
| 121 | Baane Mini Imports | Bergulfsen | Jonas  | 07-98 9555 | ... |
| 124 | Mini Gifts Distributors Ltd. | Nelson | Susan | 4155551450 | ... |
| 125 | Havel & Zbyszek Co | Piestrzeniewicz | Zbyszek  | (26) 642-7555 | ... |
| 128 | Blauer See Auto, Co. | Keitel | Roland | +49 69 66 90 2555 | ... |
| 129 | Mini Wheels Co. | Murphy | Julie | 6505555787 | ... |
| 131 | Land of Toys Inc. | Lee | Kwai | 2125557818 | ... |

*(Showing first 10 of 122 rows)*

---

### Q3. Show all orders

**SQL Query:**
```sql
SELECT * FROM orders;
```

**Execution Status:** SUCCESS

**Row Count:** 326

**Results:**

| orderNumber | orderDate | requiredDate | shippedDate | status | ... |
| --- | --- | --- | --- | --- | --- |
| 10100 | 2003-01-06 | 2003-01-13 | 2003-01-10 | Shipped | ... |
| 10101 | 2003-01-09 | 2003-01-18 | 2003-01-11 | Shipped | ... |
| 10102 | 2003-01-10 | 2003-01-18 | 2003-01-14 | Shipped | ... |
| 10103 | 2003-01-29 | 2003-02-07 | 2003-02-02 | Shipped | ... |
| 10104 | 2003-01-31 | 2003-02-09 | 2003-02-01 | Shipped | ... |
| 10105 | 2003-02-11 | 2003-02-21 | 2003-02-12 | Shipped | ... |
| 10106 | 2003-02-17 | 2003-02-24 | 2003-02-21 | Shipped | ... |
| 10107 | 2003-02-24 | 2003-03-03 | 2003-02-26 | Shipped | ... |
| 10108 | 2003-03-03 | 2003-03-12 | 2003-03-08 | Shipped | ... |
| 10109 | 2003-03-10 | 2003-03-19 | 2003-03-11 | Shipped | ... |

*(Showing first 10 of 326 rows)*

---

### Q4. List all employees

**SQL Query:**
```sql
SELECT * FROM employees;
```

**Execution Status:** SUCCESS

**Row Count:** 23

**Results:**

| employeeNumber | lastName | firstName | extension | email | ... |
| --- | --- | --- | --- | --- | --- |
| 1002 | Murphy | Diane | x5800 | dmurphy@classicmodelcars.com | ... |
| 1056 | Patterson | Mary | x4611 | mpatterso@classicmodelcars.com | ... |
| 1076 | Firrelli | Jeff | x9273 | jfirrelli@classicmodelcars.com | ... |
| 1088 | Patterson | William | x4871 | wpatterson@classicmodelcars.com | ... |
| 1102 | Bondur | Gerard | x5408 | gbondur@classicmodelcars.com | ... |
| 1143 | Bow | Anthony | x5428 | abow@classicmodelcars.com | ... |
| 1165 | Jennings | Leslie | x3291 | ljennings@classicmodelcars.com | ... |
| 1166 | Thompson | Leslie | x4065 | lthompson@classicmodelcars.com | ... |
| 1188 | Firrelli | Julie | x2173 | jfirrelli@classicmodelcars.com | ... |
| 1216 | Patterson | Steve | x4334 | spatterson@classicmodelcars.com | ... |

*(Showing first 10 of 23 rows)*

---

### Q5. Get all offices

**SQL Query:**
```sql
SELECT * FROM offices;
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| officeCode | city | phone | addressLine1 | addressLine2 | ... |
| --- | --- | --- | --- | --- | --- |
| 1 | San Francisco | +1 650 219 4782 | 100 Market Street | Suite 300 | ... |
| 2 | Boston | +1 215 837 0825 | 1550 Court Place | Suite 102 | ... |
| 3 | NYC | +1 212 555 3000 | 523 East 53rd Street | apt. 5A | ... |
| 4 | Paris | +33 14 723 4404 | 43 Rue Jouffroy Dabbans | NULL | ... |
| 5 | Tokyo | +81 33 224 5000 | 4-1 Kioicho | NULL | ... |
| 6 | Sydney | +61 2 9264 2451 | 5-11 Wentworth Avenue | Floor #2 | ... |
| 7 | London | +44 20 7877 2041 | 25 Old Broad Street | Level 7 | ... |

---

### Q6. Show all product lines

**SQL Query:**
```sql
SELECT * FROM productlines;
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| productLine | textDescription | htmlDescription | image |
| --- | --- | --- | --- |
| Classic Cars | Attention car enthusiasts: Make your wildest car o... | NULL | NULL |
| Motorcycles | Our motorcycles are state of the art replicas of c... | NULL | NULL |
| Planes | Unique, diecast airplane and helicopter replicas s... | NULL | NULL |
| Ships | The perfect holiday or anniversary gift for execut... | NULL | NULL |
| Trains | Model trains are a rewarding hobby for enthusiasts... | NULL | NULL |
| Trucks and Buses | The Truck and Bus models are realistic replicas of... | NULL | NULL |
| Vintage Cars | Our Vintage Car models realistically portray autom... | NULL | NULL |

---

### Q7. List all payments

**SQL Query:**
```sql
SELECT * FROM payments;
```

**Execution Status:** SUCCESS

**Row Count:** 273

**Results:**

| customerNumber | checkNumber | paymentDate | amount |
| --- | --- | --- | --- |
| 103 | HQ336336 | 2004-10-19 | 6066.78 |
| 103 | JM555205 | 2003-06-05 | 14571.44 |
| 103 | OM314933 | 2004-12-18 | 1676.14 |
| 112 | BO864823 | 2004-12-17 | 14191.12 |
| 112 | HQ55022 | 2003-06-06 | 32641.98 |
| 112 | ND748579 | 2004-08-20 | 33347.88 |
| 114 | GG31455 | 2003-05-20 | 45864.03 |
| 114 | MA765515 | 2004-12-15 | 82261.22 |
| 114 | NP603840 | 2003-05-31 | 7565.08 |
| 114 | NR27552 | 2004-03-10 | 44894.74 |

*(Showing first 10 of 273 rows)*

---

### Q8. Get product names and prices

**SQL Query:**
```sql
SELECT "productName", "buyPrice", "MSRP" FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 110

**Results:**

| productName | buyPrice | MSRP |
| --- | --- | --- |
| 1969 Harley Davidson Ultimate Chopper | 48.81 | 95.70 |
| 1952 Alpine Renault 1300 | 98.58 | 214.30 |
| 1996 Moto Guzzi 1100i | 68.99 | 118.94 |
| 2003 Harley-Davidson Eagle Drag Bike | 91.02 | 193.66 |
| 1972 Alfa Romeo GTA | 85.68 | 136.00 |
| 1962 LanciaA Delta 16V | 103.42 | 147.74 |
| 1968 Ford Mustang | 95.34 | 194.57 |
| 2001 Ferrari Enzo | 95.59 | 207.80 |
| 1958 Setra Bus | 77.90 | 136.67 |
| 2002 Suzuki XREO | 66.27 | 150.62 |

*(Showing first 10 of 110 rows)*

---

### Q9. Get customer names and cities

**SQL Query:**
```sql
SELECT "customerName", city FROM customers;
```

**Execution Status:** SUCCESS

**Row Count:** 122

**Results:**

| customerName | city |
| --- | --- |
| Atelier graphique | Nantes |
| Signal Gift Stores | Las Vegas |
| Australian Collectors, Co. | Melbourne |
| La Rochelle Gifts | Nantes |
| Baane Mini Imports | Stavern |
| Mini Gifts Distributors Ltd. | San Rafael |
| Havel & Zbyszek Co | Warszawa |
| Blauer See Auto, Co. | Frankfurt |
| Mini Wheels Co. | San Francisco |
| Land of Toys Inc. | NYC |

*(Showing first 10 of 122 rows)*

---

### Q10. List employee first and last names

**SQL Query:**
```sql
SELECT "firstName", "lastName" FROM employees;
```

**Execution Status:** SUCCESS

**Row Count:** 23

**Results:**

| firstName | lastName |
| --- | --- |
| Diane | Murphy |
| Mary | Patterson |
| Jeff | Firrelli |
| William | Patterson |
| Gerard | Bondur |
| Anthony | Bow |
| Leslie | Jennings |
| Leslie | Thompson |
| Julie | Firrelli |
| Steve | Patterson |

*(Showing first 10 of 23 rows)*

---

### Q11. Get all order dates

**SQL Query:**
```sql
SELECT "orderNumber", "orderDate" FROM orders;
```

**Execution Status:** SUCCESS

**Row Count:** 326

**Results:**

| orderNumber | orderDate |
| --- | --- |
| 10100 | 2003-01-06 |
| 10101 | 2003-01-09 |
| 10102 | 2003-01-10 |
| 10103 | 2003-01-29 |
| 10104 | 2003-01-31 |
| 10105 | 2003-02-11 |
| 10106 | 2003-02-17 |
| 10107 | 2003-02-24 |
| 10108 | 2003-03-03 |
| 10109 | 2003-03-10 |

*(Showing first 10 of 326 rows)*

---

### Q12. Show product vendor list

**SQL Query:**
```sql
SELECT DISTINCT "productVendor" FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 13

**Results:**

| productVendor |
| --- |
| Welly Diecast Productions |
| Motor City Art Classics |
| Classic Metal Creations |
| Studio M Art Models |
| Exoto Designs |
| Second Gear Diecast |
| Unimax Art Galleries |
| Highway 66 Mini Classics |
| Autoart Studio Design |
| Red Start Diecast |

*(Showing first 10 of 13 rows)*

---

### Q13. Get all product codes

**SQL Query:**
```sql
SELECT "productCode" FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 110

**Results:**

| productCode |
| --- |
| S10_1678 |
| S10_1949 |
| S10_2016 |
| S10_4698 |
| S10_4757 |
| S10_4962 |
| S12_1099 |
| S12_1108 |
| S12_1666 |
| S12_2823 |

*(Showing first 10 of 110 rows)*

---

### Q14. List all countries from offices

**SQL Query:**
```sql
SELECT DISTINCT country FROM offices;
```

**Execution Status:** SUCCESS

**Row Count:** 5

**Results:**

| country |
| --- |
| USA |
| France |
| Japan |
| UK |
| Australia |

---

### Q15. Show all order statuses

**SQL Query:**
```sql
SELECT DISTINCT status FROM orders;
```

**Execution Status:** SUCCESS

**Row Count:** 6

**Results:**

| status |
| --- |
| Shipped |
| In Process |
| Disputed |
| Cancelled |
| Resolved |
| On Hold |

---

### Q16. Get all payment amounts

**SQL Query:**
```sql
SELECT "checkNumber", amount, "paymentDate" FROM payments;
```

**Execution Status:** SUCCESS

**Row Count:** 273

**Results:**

| checkNumber | amount | paymentDate |
| --- | --- | --- |
| HQ336336 | 6066.78 | 2004-10-19 |
| JM555205 | 14571.44 | 2003-06-05 |
| OM314933 | 1676.14 | 2004-12-18 |
| BO864823 | 14191.12 | 2004-12-17 |
| HQ55022 | 32641.98 | 2003-06-06 |
| ND748579 | 33347.88 | 2004-08-20 |
| GG31455 | 45864.03 | 2003-05-20 |
| MA765515 | 82261.22 | 2004-12-15 |
| NP603840 | 7565.08 | 2003-05-31 |
| NR27552 | 44894.74 | 2004-03-10 |

*(Showing first 10 of 273 rows)*

---

### Q17. List all job titles

**SQL Query:**
```sql
SELECT DISTINCT "jobTitle" FROM employees;
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| jobTitle |
| --- |
| VP Sales |
| Sales Manager (APAC) |
| Sale Manager (EMEA) |
| VP Marketing |
| Sales Rep |
| Sales Manager (NA) |
| President |

---

### Q18. Get customer phone numbers

**SQL Query:**
```sql
SELECT "customerName", phone FROM customers;
```

**Execution Status:** SUCCESS

**Row Count:** 122

**Results:**

| customerName | phone |
| --- | --- |
| Atelier graphique | 40.32.2555 |
| Signal Gift Stores | 7025551838 |
| Australian Collectors, Co. | 03 9520 4555 |
| La Rochelle Gifts | 40.67.8555 |
| Baane Mini Imports | 07-98 9555 |
| Mini Gifts Distributors Ltd. | 4155551450 |
| Havel & Zbyszek Co | (26) 642-7555 |
| Blauer See Auto, Co. | +49 69 66 90 2555 |
| Mini Wheels Co. | 6505555787 |
| Land of Toys Inc. | 2125557818 |

*(Showing first 10 of 122 rows)*

---

### Q19. Show product MSRP values

**SQL Query:**
```sql
SELECT "productName", "MSRP" FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 110

**Results:**

| productName | MSRP |
| --- | --- |
| 1969 Harley Davidson Ultimate Chopper | 95.70 |
| 1952 Alpine Renault 1300 | 214.30 |
| 1996 Moto Guzzi 1100i | 118.94 |
| 2003 Harley-Davidson Eagle Drag Bike | 193.66 |
| 1972 Alfa Romeo GTA | 136.00 |
| 1962 LanciaA Delta 16V | 147.74 |
| 1968 Ford Mustang | 194.57 |
| 2001 Ferrari Enzo | 207.80 |
| 1958 Setra Bus | 136.67 |
| 2002 Suzuki XREO | 150.62 |

*(Showing first 10 of 110 rows)*

---

### Q20. List order numbers

**SQL Query:**
```sql
SELECT "orderNumber" FROM orders;
```

**Execution Status:** SUCCESS

**Row Count:** 326

**Results:**

| orderNumber |
| --- |
| 10100 |
| 10101 |
| 10102 |
| 10103 |
| 10104 |
| 10105 |
| 10106 |
| 10107 |
| 10108 |
| 10109 |

*(Showing first 10 of 326 rows)*

---

### Q21. Get orders with customer names

**SQL Query:**
```sql
SELECT o."orderNumber", o."orderDate", c."customerName" FROM orders o JOIN customers c ON o."customerNumber" = c."customerNumber";
```

**Execution Status:** SUCCESS

**Row Count:** 326

**Results:**

| orderNumber | orderDate | customerName |
| --- | --- | --- |
| 10100 | 2003-01-06 | Online Diecast Creations Co. |
| 10101 | 2003-01-09 | Blauer See Auto, Co. |
| 10102 | 2003-01-10 | Vitachrome Inc. |
| 10103 | 2003-01-29 | Baane Mini Imports |
| 10104 | 2003-01-31 | Euro+ Shopping Channel |
| 10105 | 2003-02-11 | Danish Wholesale Imports |
| 10106 | 2003-02-17 | Rovelli Gifts |
| 10107 | 2003-02-24 | Land of Toys Inc. |
| 10108 | 2003-03-03 | Cruz & Sons Co. |
| 10109 | 2003-03-10 | Motor Mint Distributors Inc. |

*(Showing first 10 of 326 rows)*

---

### Q22. Get employees with office city

**SQL Query:**
```sql
SELECT e."firstName", e."lastName", of.city FROM employees e JOIN offices of ON e."officeCode" = of."officeCode";
```

**Execution Status:** SUCCESS

**Row Count:** 23

**Results:**

| firstName | lastName | city |
| --- | --- | --- |
| Diane | Murphy | San Francisco |
| Mary | Patterson | San Francisco |
| Jeff | Firrelli | San Francisco |
| William | Patterson | Sydney |
| Gerard | Bondur | Paris |
| Anthony | Bow | San Francisco |
| Leslie | Jennings | San Francisco |
| Leslie | Thompson | San Francisco |
| Julie | Firrelli | Boston |
| Steve | Patterson | Boston |

*(Showing first 10 of 23 rows)*

---

### Q23. Get payments with customer names

**SQL Query:**
```sql
SELECT c."customerName", p."checkNumber", p.amount, p."paymentDate" FROM payments p JOIN customers c ON p."customerNumber" = c."customerNumber";
```

**Execution Status:** SUCCESS

**Row Count:** 273

**Results:**

| customerName | checkNumber | amount | paymentDate |
| --- | --- | --- | --- |
| Atelier graphique | HQ336336 | 6066.78 | 2004-10-19 |
| Atelier graphique | JM555205 | 14571.44 | 2003-06-05 |
| Atelier graphique | OM314933 | 1676.14 | 2004-12-18 |
| Signal Gift Stores | BO864823 | 14191.12 | 2004-12-17 |
| Signal Gift Stores | HQ55022 | 32641.98 | 2003-06-06 |
| Signal Gift Stores | ND748579 | 33347.88 | 2004-08-20 |
| Australian Collectors, Co. | GG31455 | 45864.03 | 2003-05-20 |
| Australian Collectors, Co. | MA765515 | 82261.22 | 2004-12-15 |
| Australian Collectors, Co. | NP603840 | 7565.08 | 2003-05-31 |
| Australian Collectors, Co. | NR27552 | 44894.74 | 2004-03-10 |

*(Showing first 10 of 273 rows)*

---

### Q24. Get order details with product names

**SQL Query:**
```sql
SELECT od."orderNumber", pr."productName", od."quantityOrdered", od."priceEach" FROM orderdetails od JOIN products pr ON od."productCode" = pr."productCode";
```

**Execution Status:** SUCCESS

**Row Count:** 2996

**Results:**

| orderNumber | productName | quantityOrdered | priceEach |
| --- | --- | --- | --- |
| 10100 | 1917 Grand Touring Sedan | 30 | 136.00 |
| 10100 | 1911 Ford Town Car | 50 | 55.09 |
| 10100 | 1932 Alfa Romeo 8C2300 Spider Sport | 22 | 75.46 |
| 10100 | 1936 Mercedes Benz 500k Roadster | 49 | 35.29 |
| 10101 | 1932 Model A Ford J-Coupe | 25 | 108.06 |
| 10101 | 1928 Mercedes-Benz SSK | 26 | 167.06 |
| 10101 | 1939 Chevrolet Deluxe Coupe | 45 | 32.53 |
| 10101 | 1938 Cadillac V-16 Presidential Limousine | 46 | 44.35 |
| 10102 | 1937 Lincoln Berline | 39 | 95.55 |
| 10102 | 1936 Mercedes-Benz 500K Special Roadster | 41 | 43.13 |

*(Showing first 10 of 2996 rows)*

---

### Q25. Get products with product line description

**SQL Query:**
```sql
SELECT pr."productName", pl."textDescription" FROM products pr JOIN productlines pl ON pr."productLine" = pl."productLine";
```

**Execution Status:** SUCCESS

**Row Count:** 110

**Results:**

| productName | textDescription |
| --- | --- |
| 1969 Harley Davidson Ultimate Chopper | Our motorcycles are state of the art replicas of c... |
| 1952 Alpine Renault 1300 | Attention car enthusiasts: Make your wildest car o... |
| 1996 Moto Guzzi 1100i | Our motorcycles are state of the art replicas of c... |
| 2003 Harley-Davidson Eagle Drag Bike | Our motorcycles are state of the art replicas of c... |
| 1972 Alfa Romeo GTA | Attention car enthusiasts: Make your wildest car o... |
| 1962 LanciaA Delta 16V | Attention car enthusiasts: Make your wildest car o... |
| 1968 Ford Mustang | Attention car enthusiasts: Make your wildest car o... |
| 2001 Ferrari Enzo | Attention car enthusiasts: Make your wildest car o... |
| 1958 Setra Bus | The Truck and Bus models are realistic replicas of... |
| 2002 Suzuki XREO | Our motorcycles are state of the art replicas of c... |

*(Showing first 10 of 110 rows)*

---

### Q26. Get customers with sales rep names

**SQL Query:**
```sql
SELECT c."customerName", e."firstName" || ' ' || e."lastName" AS "salesRepName" FROM customers c JOIN employees e ON c."salesRepEmployeeNumber" = e."employeeNumber";
```

**Execution Status:** SUCCESS

**Row Count:** 100

**Results:**

| customerName | salesRepName |
| --- | --- |
| Atelier graphique | Gerard Hernandez |
| Signal Gift Stores | Leslie Thompson |
| Australian Collectors, Co. | Andy Fixter |
| La Rochelle Gifts | Gerard Hernandez |
| Baane Mini Imports | Barry Jones |
| Mini Gifts Distributors Ltd. | Leslie Jennings |
| Blauer See Auto, Co. | Barry Jones |
| Mini Wheels Co. | Leslie Jennings |
| Land of Toys Inc. | George Vanauf |
| Euro+ Shopping Channel | Gerard Hernandez |

*(Showing first 10 of 100 rows)*

---

### Q27. Get orders with customer city

**SQL Query:**
```sql
SELECT o."orderNumber", o."orderDate", c.city FROM orders o JOIN customers c ON o."customerNumber" = c."customerNumber";
```

**Execution Status:** SUCCESS

**Row Count:** 326

**Results:**

| orderNumber | orderDate | city |
| --- | --- | --- |
| 10100 | 2003-01-06 | Nashua |
| 10101 | 2003-01-09 | Frankfurt |
| 10102 | 2003-01-10 | NYC |
| 10103 | 2003-01-29 | Stavern |
| 10104 | 2003-01-31 | Madrid |
| 10105 | 2003-02-11 | Kobenhavn |
| 10106 | 2003-02-17 | Bergamo |
| 10107 | 2003-02-24 | NYC |
| 10108 | 2003-03-03 | Makati City |
| 10109 | 2003-03-10 | Philadelphia |

*(Showing first 10 of 326 rows)*

---

### Q28. Get employees and their manager

**SQL Query:**
```sql
SELECT e."firstName" || ' ' || e."lastName" AS employee, m."firstName" || ' ' || m."lastName" AS manager FROM employees e LEFT JOIN employees m ON e."reportsTo" = m."employeeNumber";
```

**Execution Status:** SUCCESS

**Row Count:** 23

**Results:**

| employee | manager |
| --- | --- |
| Diane Murphy | NULL |
| Mary Patterson | Diane Murphy |
| Jeff Firrelli | Diane Murphy |
| William Patterson | Mary Patterson |
| Gerard Bondur | Mary Patterson |
| Anthony Bow | Mary Patterson |
| Leslie Jennings | Anthony Bow |
| Leslie Thompson | Anthony Bow |
| Julie Firrelli | Anthony Bow |
| Steve Patterson | Anthony Bow |

*(Showing first 10 of 23 rows)*

---

### Q29. Get order details with product vendor

**SQL Query:**
```sql
SELECT od."orderNumber", pr."productVendor", od."quantityOrdered" FROM orderdetails od JOIN products pr ON od."productCode" = pr."productCode";
```

**Execution Status:** SUCCESS

**Row Count:** 2996

**Results:**

| orderNumber | productVendor | quantityOrdered |
| --- | --- | --- |
| 10100 | Welly Diecast Productions | 30 |
| 10100 | Motor City Art Classics | 50 |
| 10100 | Exoto Designs | 22 |
| 10100 | Red Start Diecast | 49 |
| 10101 | Autoart Studio Design | 25 |
| 10101 | Gearbox Collectibles | 26 |
| 10101 | Motor City Art Classics | 45 |
| 10101 | Classic Metal Creations | 46 |
| 10102 | Motor City Art Classics | 39 |
| 10102 | Studio M Art Models | 41 |

*(Showing first 10 of 2996 rows)*

---

### Q30. Get payments with customer country

**SQL Query:**
```sql
SELECT p."checkNumber", p.amount, c.country FROM payments p JOIN customers c ON p."customerNumber" = c."customerNumber";
```

**Execution Status:** SUCCESS

**Row Count:** 273

**Results:**

| checkNumber | amount | country |
| --- | --- | --- |
| HQ336336 | 6066.78 | France |
| JM555205 | 14571.44 | France |
| OM314933 | 1676.14 | France |
| BO864823 | 14191.12 | USA |
| HQ55022 | 32641.98 | USA |
| ND748579 | 33347.88 | USA |
| GG31455 | 45864.03 | Australia |
| MA765515 | 82261.22 | Australia |
| NP603840 | 7565.08 | Australia |
| NR27552 | 44894.74 | Australia |

*(Showing first 10 of 273 rows)*

---

### Q31. Count customers per country

**SQL Query:**
```sql
SELECT country, COUNT("customerNumber") AS customer_count FROM customers GROUP BY country ORDER BY customer_count DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 28

**Results:**

| country | customer_count |
| --- | --- |
| USA | 36 |
| Germany | 13 |
| France | 12 |
| Spain | 7 |
| UK | 5 |
| Australia | 5 |
| Italy | 4 |
| New Zealand | 4 |
| Switzerland | 3 |
| Singapore | 3 |

*(Showing first 10 of 28 rows)*

---

### Q32. Total payments per customer

**SQL Query:**
```sql
SELECT c."customerName", SUM(p.amount) AS total_paid FROM payments p JOIN customers c ON p."customerNumber" = c."customerNumber" GROUP BY c."customerName" ORDER BY total_paid DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 98

**Results:**

| customerName | total_paid |
| --- | --- |
| Euro+ Shopping Channel | 715738.98 |
| Mini Gifts Distributors Ltd. | 584188.24 |
| Australian Collectors, Co. | 180585.07 |
| Muscle Machine Inc | 177913.95 |
| Dragon Souveniers, Ltd. | 156251.03 |
| Down Under Souveniers, Inc | 154622.08 |
| AV Stores, Co. | 148410.09 |
| Anna's Decorations, Ltd | 137034.22 |
| Corporate Gift Ideas Co. | 132340.78 |
| Saveley & Henriot, Co. | 130305.35 |

*(Showing first 10 of 98 rows)*

---

### Q33. Number of orders per status

**SQL Query:**
```sql
SELECT status, COUNT("orderNumber") AS order_count FROM orders GROUP BY status;
```

**Execution Status:** SUCCESS

**Row Count:** 6

**Results:**

| status | order_count |
| --- | --- |
| Shipped | 303 |
| In Process | 6 |
| Disputed | 3 |
| Cancelled | 6 |
| Resolved | 4 |
| On Hold | 4 |

---

### Q34. Products per product line

**SQL Query:**
```sql
SELECT "productLine", COUNT("productCode") AS product_count FROM products GROUP BY "productLine" ORDER BY product_count DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| productLine | product_count |
| --- | --- |
| Classic Cars | 38 |
| Vintage Cars | 24 |
| Motorcycles | 13 |
| Planes | 12 |
| Trucks and Buses | 11 |
| Ships | 9 |
| Trains | 3 |

---

### Q35. Employees per office

**SQL Query:**
```sql
SELECT of.city, COUNT(e."employeeNumber") AS employee_count FROM employees e JOIN offices of ON e."officeCode" = of."officeCode" GROUP BY of.city ORDER BY employee_count DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| city | employee_count |
| --- | --- |
| San Francisco | 6 |
| Paris | 5 |
| Sydney | 4 |
| Tokyo | 2 |
| Boston | 2 |
| London | 2 |
| NYC | 2 |

---

### Q36. Total stock per product vendor

**SQL Query:**
```sql
SELECT "productVendor", SUM("quantityInStock") AS total_stock FROM products GROUP BY "productVendor" ORDER BY total_stock DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 13

**Results:**

| productVendor | total_stock |
| --- | --- |
| Gearbox Collectibles | 60495 |
| Min Lin Diecast | 50089 |
| Classic Metal Creations | 45408 |
| Welly Diecast Productions | 45095 |
| Exoto Designs | 44166 |
| Motor City Art Classics | 43105 |
| Second Gear Diecast | 42865 |
| Studio M Art Models | 42253 |
| Carousel DieCast Legends | 40805 |
| Unimax Art Galleries | 38191 |

*(Showing first 10 of 13 rows)*

---

### Q37. Average buy price per product line

**SQL Query:**
```sql
SELECT "productLine", ROUND(AVG("buyPrice"), 2) AS avg_buy_price FROM products GROUP BY "productLine" ORDER BY avg_buy_price DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| productLine | avg_buy_price |
| --- | --- |
| Classic Cars | 64.45 |
| Trucks and Buses | 56.33 |
| Motorcycles | 50.69 |
| Planes | 49.63 |
| Ships | 47.01 |
| Vintage Cars | 46.07 |
| Trains | 43.92 |

---

### Q38. Orders per customer

**SQL Query:**
```sql
SELECT c."customerName", COUNT(o."orderNumber") AS order_count FROM orders o JOIN customers c ON o."customerNumber" = c."customerNumber" GROUP BY c."customerName" ORDER BY order_count DESC;
```

**Execution Status:** SUCCESS

**Row Count:** 98

**Results:**

| customerName | order_count |
| --- | --- |
| Euro+ Shopping Channel | 26 |
| Mini Gifts Distributors Ltd. | 17 |
| Dragon Souveniers, Ltd. | 5 |
| Australian Collectors, Co. | 5 |
| Down Under Souveniers, Inc | 5 |
| Reims Collectables | 5 |
| Danish Wholesale Imports | 5 |
| Volvo Model Replicas, Co | 4 |
| Anna's Decorations, Ltd | 4 |
| Technics Stores Inc. | 4 |

*(Showing first 10 of 98 rows)*

---

### Q39. Max MSRP per product line

**SQL Query:**
```sql
SELECT "productLine", MAX("MSRP") AS max_msrp FROM products GROUP BY "productLine";
```

**Execution Status:** SUCCESS

**Row Count:** 7

**Results:**

| productLine | max_msrp |
| --- | --- |
| Classic Cars | 214.30 |
| Trains | 100.84 |
| Planes | 157.69 |
| Trucks and Buses | 136.67 |
| Vintage Cars | 170.00 |
| Motorcycles | 193.66 |
| Ships | 122.89 |

---

### Q40. Min buy price per vendor

**SQL Query:**
```sql
SELECT "productVendor", MIN("buyPrice") AS min_buy_price FROM products GROUP BY "productVendor";
```

**Execution Status:** SUCCESS

**Row Count:** 13

**Results:**

| productVendor | min_buy_price |
| --- | --- |
| Welly Diecast Productions | 24.23 |
| Motor City Art Classics | 22.57 |
| Classic Metal Creations | 20.61 |
| Studio M Art Models | 23.14 |
| Exoto Designs | 43.26 |
| Second Gear Diecast | 16.24 |
| Unimax Art Galleries | 33.30 |
| Highway 66 Mini Classics | 32.37 |
| Autoart Studio Design | 26.30 |
| Red Start Diecast | 21.75 |

*(Showing first 10 of 13 rows)*

---

### Q41. Total number of customers

**SQL Query:**
```sql
SELECT COUNT("customerNumber") AS total_customers FROM customers;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| total_customers |
| --- |
| 122 |

---

### Q42. Total number of products

**SQL Query:**
```sql
SELECT COUNT("productCode") AS total_products FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| total_products |
| --- |
| 110 |

---

### Q43. Total revenue from payments

**SQL Query:**
```sql
SELECT SUM(amount) AS total_revenue FROM payments;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| total_revenue |
| --- |
| 8853839.23 |

---

### Q44. Average product price

**SQL Query:**
```sql
SELECT ROUND(AVG("buyPrice"), 2) AS avg_buy_price FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| avg_buy_price |
| --- |
| 54.40 |

---

### Q45. Max payment amount

**SQL Query:**
```sql
SELECT MAX(amount) AS max_payment FROM payments;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| max_payment |
| --- |
| 120166.58 |

---

### Q46. Min payment amount

**SQL Query:**
```sql
SELECT MIN(amount) AS min_payment FROM payments;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| min_payment |
| --- |
| 615.45 |

---

### Q47. Count total orders

**SQL Query:**
```sql
SELECT COUNT("orderNumber") AS total_orders FROM orders;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| total_orders |
| --- |
| 326 |

---

### Q48. Total quantity in stock

**SQL Query:**
```sql
SELECT SUM("quantityInStock") AS total_stock FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| total_stock |
| --- |
| 555131 |

---

### Q49. Average MSRP

**SQL Query:**
```sql
SELECT ROUND(AVG("MSRP"), 2) AS avg_msrp FROM products;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| avg_msrp |
| --- |
| 100.44 |

---

### Q50. Number of employees

**SQL Query:**
```sql
SELECT COUNT("employeeNumber") AS total_employees FROM employees;
```

**Execution Status:** SUCCESS

**Row Count:** 1

**Results:**

| total_employees |
| --- |
| 23 |

---


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

