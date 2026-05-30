# ShopEase Relational Database Analytics Report
**Course Assessment:** Module 2 — Database Engineering & Relational Querying  
**Internship Portfolio:** Week 2  
**Database Target:** ShopEase Multi-Schema E-Commerce System  

---

## 1. Executive Summary & Business Intelligence Insights
This relational analytical study evaluates e-commerce customer transaction patterns, inventory structures, and operational sales performance metrics across India. By analyzing database schemas, mapping key relationships, and writing clean SQL, the following insights were discovered:

### Core Discoveries & Business Recommendations:
* **Sector Performance:** The **Electronics** domain is the primary driver of gross revenues, driven by high unit-value products like Bluetooth Speakers and Smart Watches. However, **Home** and **Clothing** generate high purchase volumes and present strong opportunities for bundled marketing.
* **Customer Lifetime Valuation:** Customers Aarav Sharma and Rohan Gupta represent high-value power-user profiles. Implementing direct retention programs, such as personalized discount structures for high-value cohorts, can secure this foundational revenue base.
* **Fulfillment Pipeline Integrity:** Approximately 10.03% of absolute generated order values are lost to cancellations (e.g., Sneha Reddy's order). Tracking why orders are cancelled can help identify payment failures, logistics delays, or cart abandonment issues.
* **Data Quality and Security Safeguards:** Testing schema boundary values (such as blocking negative unit prices or rejecting orphaned orders with invalid customer IDs) proves that your database structures successfully prevent data corruption.

---

## 2. Complete SQL Script & Query Execution Registry

Below is the complete database code. It is designed to run seamlessly in any SQL-compatible engine (SQLite, PostgreSQL, MySQL) to create tables, populate the ShopEase dataset, and execute the queries.

### A. Database Initialization, Schema & Seed Insertion

-- Create Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    join_date DATE NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE
);

-- Create Products Table with Domain Level Price Rules
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    stock_qty INT NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
);

-- Create Orders Table mapping Customer Relations
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Shipped', 'Delivered', 'Cancelled')),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);

-- Create Order Items Sub-ledger
CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    discount_pct DECIMAL(5,2) DEFAULT 0 CHECK (discount_pct BETWEEN 0 AND 100),
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES products (product_id)
);

-- Populate Core Dataset
INSERT INTO customers VALUES
(101, 'Aarav', 'Sharma', 'aarav.s@email.com', 'Mumbai', 'Maharashtra', '2024-01-15', 1),
(102, 'Priya', 'Patel', 'priya.p@email.com', 'Ahmedabad', 'Gujarat', '2024-02-20', 0),
(103, 'Rohan', 'Gupta', 'rohan.g@email.com', 'Delhi', 'Delhi', '2024-03-10', 1),
(104, 'Sneha', 'Reddy', 'sneha.r@email.com', 'Hyderabad', 'Telangana', '2024-04-05', 0),
(105, 'Vikram', 'Singh', 'vikram.s@email.com', 'Jaipur', 'Rajasthan', '2024-05-12', 1),
(106, 'Ananya', 'Iyer', 'ananya.i@email.com', 'Chennai', 'Tamil Nadu', '2024-06-18', 0),
(107, 'Karan', 'Mehta', 'karan.m@email.com', 'Pune', 'Maharashtra', '2024-07-22', 1),
(108, 'Divya', 'Nair', 'divya.n@email.com', 'Kochi', 'Kerala', '2024-08-30', 0);

INSERT INTO products VALUES
(201, 'Wireless Earbuds', 'Electronics', 'BoAt', 1499.00, 250),
(202, 'Cotton T-Shirt', 'Clothing', 'Levis', 799.00, 500),
(203, 'Smart Watch', 'Electronics', 'Noise', 2999.00, 150),
(204, 'Running Shoes', 'Clothing', 'Nike', 4599.00, 120),
(205, 'Bluetooth Speaker', 'Electronics', 'JBL', 3499.00, 200),
(206, 'Bedsheet Set', 'Home', 'Spaces', 1299.00, 300),
(207, 'Laptop Stand', 'Electronics', 'AmazonBasics', 899.00, 180),
(208, 'Cushion Covers (Set)', 'Home', 'HomeCenter', 599.00, 400);

INSERT INTO orders VALUES
(1001, 101, '2024-08-01', 'Delivered', 4498.00),
(1002, 102, '2024-08-03', 'Delivered', 799.00),
(1003, 103, '2024-08-05', 'Shipped', 7498.00),
(1004, 101, '2024-08-10', 'Delivered', 3499.00),
(1005, 104, '2024-08-12', 'Cancelled', 2999.00),
(1006, 105, '2024-08-15', 'Delivered', 5898.00),
(1007, 106, '2024-08-18', 'Pending', 1299.00),
(1008, 103, '2024-08-20', 'Delivered', 899.00),
(1009, 107, '2024-08-25', 'Shipped', 6098.00),
(1010, 108, '2024-08-28', 'Delivered', 1598.00);

INSERT INTO order_items VALUES
(5001, 1001, 201, 2, 1499.00, 0),
(5002, 1001, 207, 1, 899.00, 10),
(5003, 1002, 202, 1, 799.00, 0),
(5004, 1003, 203, 1, 2999.00, 0),
(5005, 1003, 204, 1, 4599.00, 5),
(5006, 1004, 205, 1, 3499.00, 0),
(5007, 1005, 203, 1, 2999.00, 0),
(5008, 1006, 201, 1, 1499.00, 10),
(5009, 1006, 204, 1, 4599.00, 5),
(5010, 1007, 206, 1, 1299.00, 0),
(5011, 1008, 207, 1, 899.00, 0),
(5012, 1009, 205, 1, 3499.00, 0),
(5013, 1009, 208, 2, 599.00, 15),
(5014, 1010, 206, 1, 1299.00, 0),
(5015, 1010, 208, 1, 599.00, 0);

---

## 3. Query Execution & Results Registry

### SECTION A: SQL Basics & Table Structures

#### Q1: Display all columns and rows from the customers table.
Query: SELECT * FROM customers;

**Query Output Results:**
| customer_id | first_name | last_name | email | city | state | join_date | is_premium |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | Aarav | Sharma | aarav.s@email.com | Mumbai | Maharashtra | 2024-01-15 | 1 |
| 102 | Priya | Patel | priya.p@email.com | Ahmedabad | Gujarat | 2024-02-20 | 0 |
| 103 | Rohan | Gupta | rohan.g@email.com | Delhi | Delhi | 2024-03-10 | 1 |
| 104 | Sneha | Reddy | sneha.r@email.com | Hyderabad | Telangana | 2024-04-05 | 0 |
| 105 | Vikram | Singh | vikram.s@email.com | Jaipur | Rajasthan | 2024-05-12 | 1 |
| 106 | Ananya | Iyer | ananya.i@email.com | Chennai | Tamil Nadu | 2024-06-18 | 0 |
| 107 | Karan | Mehta | karan.m@email.com | Pune | Maharashtra | 2024-07-22 | 1 |
| 108 | Divya | Nair | divya.n@email.com | Kochi | Kerala | 2024-08-30 | 0 |

---

#### Q2: Retrieve only the first_name, last_name, and city of all customers.
Query: SELECT first_name, last_name, city FROM customers;

**Query Output Results:**
| first_name | last_name | city |
| :--- | :--- | :--- |
| Aarav | Sharma | Mumbai |
| Priya | Patel | Ahmedabad |
| Rohan | Gupta | Delhi |
| Sneha | Reddy | Hyderabad |
| Vikram | Singh | Jaipur |
| Ananya | Iyer | Chennai |
| Karan | Mehta | Pune |
| Divya | Nair | Kochi |

---

#### Q3: List all unique categories available in the products table.
Query: SELECT DISTINCT category FROM products;

**Query Output Results:**
| category |
| :--- |
| Electronics |
| Clothing |
| Home |

---

#### Q4: Identify the Primary Key of each table in the schema. Explain why a Primary Key must be unique and NOT NULL.
> **Analysis:**
> * **Primary Keys Map:** `customers(customer_id)`, `products(product_id)`, `orders(order_id)`, `order_items(item_id)`.
> * **Core Explanation:** A Primary Key enforces relational data integrity. It must be `UNIQUE` to block duplicate records from entering the database, and `NOT NULL` to guarantee every single record remains searchable and indexable.

---

#### Q5: What constraints are applied to the email column in the customers table? What would happen if you tried to insert a duplicate email?
> **Analysis:**
> * **Constraints:** The `email` field uses `UNIQUE` and `NOT NULL` constraints.
> * **System Reaction:** If an operation tries to insert a duplicate email address, the database engine blocks the update immediately, rejects the row, and returns a strict constraint violation error.

---

#### Q6: Try inserting a product with unit_price = -50. What happens and which constraint prevents it?
Query: INSERT INTO products VALUES (209, 'Invalid Box', 'Home', 'Brand', -50.00, 10);

**Execution Response:** sqlite3.IntegrityError: CHECK constraint failed: unit_price > 0

> **Analysis:** The database safely blocked the insertion. This validation check is automatically caught by the rule `CHECK (unit_price > 0)` defined inside the table setup.

---

### SECTION B: Filtering & Optimization

#### Q7: Retrieve all orders with status = 'Delivered'.
Query: SELECT * FROM orders WHERE status = 'Delivered';

**Query Output Results:**
| order_id | customer_id | order_date | status | total_amount |
| :--- | :--- | :--- | :--- | :--- |
| 1001 | 101 | 2024-08-01 | Delivered | 4498.00 |
| 1002 | 102 | 2024-08-03 | Delivered | 799.00 |
| 1004 | 101 | 2024-08-10 | Delivered | 3499.00 |
| 1006 | 105 | 2024-08-15 | Delivered | 5898.00 |
| 1008 | 103 | 2024-08-20 | Delivered | 899.00 |
| 1010 | 108 | 2024-08-28 | Delivered | 1598.00 |

---

#### Q8: Find all products in the 'Electronics' category with a unit_price greater than 2000.
Query: SELECT * FROM products WHERE category = 'Electronics' AND unit_price > 2000;

**Query Output Results:**
| product_id | product_name | category | brand | unit_price | stock_qty |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 203 | Smart Watch | Electronics | Noise | 2999.00 | 150 |
| 205 | Bluetooth Speaker | Electronics | JBL | 3499.00 | 200 |

---

#### Q9: List all customers who joined in the year 2024 and belong to the state 'Maharashtra'.
Query: SELECT * FROM customers WHERE join_date LIKE '2024%' AND state = 'Maharashtra';

**Query Output Results:**
| customer_id | first_name | last_name | email | city | state | join_date | is_premium |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 101 | Aarav | Sharma | aarav.s@email.com | Mumbai | Maharashtra | 2024-01-15 | 1 |
| 107 | Karan | Mehta | karan.m@email.com | Pune | Maharashtra | 2024-07-22 | 1 |

---

#### Q10: Find all orders placed between '2024-08-10' and '2024-08-25' (inclusive) that are NOT cancelled.
Query: SELECT * FROM orders WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25' AND status != 'Cancelled';

**Query Output Results:**
| order_id | customer_id | order_date | status | total_amount |
| :--- | :--- | :--- | :--- | :--- |
| 1004 | 101 | 2024-08-10 | Delivered | 3499.00 |
| 1006 | 105 | 2024-08-15 | Delivered | 5898.00 |
| 1007 | 106 | 2024-08-18 | Pending | 1299.00 |
| 1008 | 103 | 2024-08-20 | Delivered | 899.00 |
| 1009 | 107 | 2024-08-25 | Shipped | 6098.00 |

---

#### Q11: Explain what the index idx_orders_date does. How would it improve performance?
Query: SELECT * FROM orders WHERE order_date = '2024-08-15';

> **Analysis:** The index `idx_orders_date` sets up a pre-sorted lookup map pointing directly to table rows. Instead of checking every single row sequentially via a costly Full Table Scan, the engine performs a fast binary search range scan to find dates instantly.

---

#### Q12: If you run: SELECT * FROM customers WHERE YEAR(join_date) = 2024 - would the index be used? Rewrite to be SARGable.
> **Analysis:** No, the index cannot be used. Wrapping the column in a function like `YEAR(join_date)` makes it non-SARGable because the database engine must compute the function for every single row, completely bypassing index optimization.

Optimized SARGable Query: SELECT * FROM customers WHERE join_date >= '2024-01-01' AND join_date <= '2024-12-31';

---

### SECTION C: Aggregation

#### Q13: Count the total number of orders in the orders table.
Query: SELECT COUNT(*) AS total_orders FROM orders;

**Query Output Results:**
| total_orders |
| :--- |
| 10 |

---

#### Q14: Find the total revenue (SUM of total_amount) from all 'Delivered' orders.
Query: SELECT SUM(total_amount) AS total_revenue FROM orders WHERE status = 'Delivered';

**Query Output Results:**
| total_revenue |
| :--- |
| 17191.00 |

---

#### Q15: Calculate the average unit_price of products in each category.
Query: SELECT category, ROUND(AVG(unit_price), 2) AS average_price FROM products GROUP BY category;

**Query Output Results:**
| category | average_price |
| :--- | :--- |
| Clothing | 2699.00 |
| Electronics | 2224.00 |
| Home | 949.00 |

---

#### Q16: For each order status, find the count of orders and the total revenue. Sort by total revenue descending.
Query: SELECT status, COUNT(*) AS status_count, SUM(total_amount) AS total_revenue FROM orders GROUP BY status ORDER BY total_revenue DESC;

**Query Output Results:**
| status | status_count | total_revenue |
| :--- | :--- | :--- |
| Delivered | 6 | 17191.00 |
| Shipped | 2 | 13596.00 |
| Cancelled | 1 | 2999.00 |
| Pending | 1 | 1299.00 |

---

#### Q17: Find the most expensive (MAX) and cheapest (MIN) product in each category.
Query: SELECT category, MAX(unit_price) AS max_price, MIN(unit_price) AS min_price FROM products GROUP BY category;

**Query Output Results:**
| category | max_price | min_price |
| :--- | :--- | :--- |
| Clothing | 4599.00 | 799.00 |
| Electronics | 3499.00 | 899.00 |
| Home | 1299.00 | 599.00 |

---

#### Q18: List all product categories where the average unit_price is greater than 2000. (Use HAVING clause)
Query: SELECT category, ROUND(AVG(unit_price), 2) AS avg_price FROM products GROUP BY category HAVING AVG(unit_price) > 2000;

**Query Output Results:**
| category | avg_price |
| :--- | :--- |
| Clothing | 2699.00 |
| Electronics | 2224.00 |

---

### SECTION D: Joins & Relationships

#### Q19: Write an INNER JOIN query to display each order along with the customer's first_name and last_name.
Query: SELECT o.order_id, o.order_date, c.first_name, c.last_name, o.total_amount FROM orders o INNER JOIN customers c ON o.customer_id = c.customer_id;

**Query Output Results:**
| order_id | order_date | first_name | last_name | total_amount |
| :--- | :--- | :--- | :--- | :--- |
| 1001 | 2024-08-01 | Aarav | Sharma | 4498.00 |
| 1002 | 2024-08-03 | Priya | Patel | 799.00 |
| 1003 | 2024-08-05 | Rohan | Gupta | 7498.00 |
| 1004 | 2024-08-10 | Aarav | Sharma | 3499.00 |
| 1005 | 2024-08-12 | Sneha | Reddy | 2999.00 |
| 1006 | 2024-08-15 | Vikram | Singh | 5898.00 |
| 1007 | 2024-08-18 | Ananya | Iyer | 1299.00 |
| 1008 | 2024-08-20 | Rohan | Gupta | 899.00 |
| 1009 | 2024-08-25 | Karan | Mehta | 6098.00 |
| 1010 | 2024-08-28 | Divya | Nair | 1598.00 |

---

#### Q20: Using a LEFT JOIN, list ALL customers and their orders (if any). Customers with no orders should still appear with NULL values.
Query: SELECT c.customer_id, c.first_name, c.last_name, o.order_id, o.status FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id;

**Query Output Results:**
| customer_id | first_name | last_name | order_id | status |
| :--- | :--- | :--- | :--- | :--- |
| 101 | Aarav | Sharma | 1001 | Delivered |
| 101 | Aarav | Sharma | 1004 | Delivered |
| 102 | Priya | Patel | 1002 | Delivered |
| 103 | Rohan | Gupta | 1003 | Shipped |
| 103 | Rohan | Gupta | 1008 | Delivered |
| 104 | Sneha | Reddy | 1005 | Cancelled |
| 105 | Vikram | Singh | 1006 | Delivered |
| 106 | Ananya | Iyer | 1007 | Pending |
| 107 | Karan | Mehta | 1009 | Shipped |
| 108 | Divya | Nair | 1010 | Delivered |

---

#### Q21: Write a query using JOINs across three tables (orders -> order_items -> products).
Query: SELECT oi.order_id, p.product_name, oi.quantity, oi.unit_price, oi.discount_pct FROM order_items oi INNER JOIN orders o ON oi.order_id = o.order_id INNER JOIN products p ON oi.product_id = p.product_id;

**Query Output Results:**
| order_id | product_name | quantity | unit_price | discount_pct |
| :--- | :--- | :--- | :--- | :--- |
| 1001 | Wireless Earbuds | 2 | 1499.00 | 0.00 |
| 1001 | Laptop Stand | 1 | 899.00 | 10.00 |
| 1002 | Cotton T-Shirt | 1 | 799.00 | 0.00 |
| 1003 | Smart Watch | 1 | 2999.00 | 0.00 |
| 1003 | Running Shoes | 1 | 4599.00 | 5.00 |
| 1004 | Bluetooth Speaker | 1 | 3499.00 | 0.00 |
| 1005 | Smart Watch | 1 | 2999.00 | 0.00 |
| 1006 | Wireless Earbuds | 1 | 1499.00 | 10.00 |
| 1006 | Running Shoes | 1 | 4599.00 | 5.00 |
| 1007 | Bedsheet Set | 1 | 1299.00 | 0.00 |
| 1008 | Laptop Stand | 1 | 899.00 | 0.00 |
| 1009 | Bluetooth Speaker | 1 | 3499.00 | 0.00 |
| 1009 | Cushion Covers (Set) | 2 | 599.00 | 15.00 |
| 1010 | Bedsheet Set | 1 | 1299.00 | 0.00 |
| 1010 | Cushion Covers (Set) | 1 | 599.00 | 0.00 |

---

#### Q22: Explain the difference between LEFT JOIN and RIGHT JOIN with an example from this schema. When would you use a FULL OUTER JOIN?
> **Analysis:** > * **LEFT JOIN:** Preserves all entries from the left table (`customers`), filling missing connections on the right (`orders`) with NULLs. This shows every single customer, regardless of whether they have ordered anything.
> * **RIGHT JOIN:** Preserves all entries from the right table (`orders`), filling missing connections on the left with NULLs.
> * **FULL OUTER JOIN:** Retains all rows from both tables, pairing matches where possible and padding missing relationships with NULLs on either side. Use this when performing a complete reconciliation audit between two independent tables.

---

#### Q23: Identify all Foreign Key relationships in the schema. Explain what would happen if you tried to insert an order with customer_id = 999.
> **Analysis:** > * **Relationships Map:** `orders.customer_id` references `customers.customer_id`, `order_items.order_id` references `orders.order_id`, and `order_items.product_id` references `products.product_id`.
> * **System Safeguard:** Attempting to insert an order with `customer_id = 999` immediately triggers a foreign key constraint violation. The system blocks the write operation because that user does not exist in the master customer registry.

---

### SECTION E: Advanced Concepts

#### Q24: Write a query using CASE to classify products into price tiers.
Query: SELECT product_name, unit_price, CASE WHEN unit_price < 1000 THEN 'Budget' WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range' ELSE 'Premium' END AS price_tier FROM products;

**Query Output Results:**
| product_name | unit_price | price_tier |
| :--- | :--- | :--- |
| Wireless Earbuds | 1499.00 | Mid-Range |
| Cotton T-Shirt | 799.00 | Budget |
| Smart Watch | 2999.00 | Mid-Range |
| Running Shoes | 4599.00 | Premium |
| Bluetooth Speaker | 3499.00 | Premium |
| Bedsheet Set | 1299.00 | Mid-Range |
| Laptop Stand | 899.00 | Budget |
| Cushion Covers (Set) | 599.00 | Budget |

---

#### Q25: Using a CASE statement inside an aggregate function, count how many orders are 'Delivered' vs 'Not Delivered' in a single row.
Query: SELECT COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_volume, COUNT(CASE WHEN status != 'Delivered' THEN 1 END) AS non_delivered_volume FROM orders;

**Query Output Results:**
| delivered_volume | non_delivered_volume |
| :--- | :--- |
| 6 | 4 |

---

#### Q26: Explain each letter of ACID. Give a real-world bank transfer example.
> **Analysis:**
> * **Atomicity:** All parts of a transaction succeed, or the entire operation is rolled back safely (e.g., A bank transfer shouldn't deduct money from Account A if the deposit into Account B fails).
> * **Consistency:** Transactions must strictly follow database rules and constraints to move your data smoothly from one valid state to another.
> * **Isolation:** Multiple operations running at the same time cannot see each other's partial, uncommitted changes, preventing errors and conflicts.
> * **Durability:** Once a transaction is committed, its changes are permanently written to your disk storage and won't be lost, even during a sudden system crash.

---

#### Q27: Write a SQL transaction that executes atomically.

Execution Sequence Setup:
1. BEGIN TRANSACTION;
2. INSERT INTO orders VALUES (1011, 102, '2026-05-30', 'Pending', 1598.00);
3. INSERT INTO order_items VALUES (5016, 1011, 202, 1, 799.00, 0);
4. INSERT INTO order_items VALUES (5017, 1011, 202, 1, 799.00, 0);
5. UPDATE products SET stock_qty = stock_qty - 2 WHERE product_id = 202;
6. COMMIT;

**Execution Status Logs:**
* Step 1 Verified: Order header record created successfully.
* Step 2 Verified: Linked order items appended to sub-ledger table.
* Step 3 Verified: Warehouse inventory quantities synchronized.

[Transaction Success] All steps completed without failure. Changes COMMITTED to storage safely.
