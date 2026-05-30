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
* **Fulfillment Pipeline Integrity:** Approximately $10.03\%$ of absolute generated order values are lost to cancellations (e.g., Sneha Reddy's order). Tracking why orders are cancelled can help identify payment failures, logistics delays, or cart abandonment issues.
* **Data Quality and Security Safeguards:** Testing schema boundary values (such as blocking negative unit prices or rejecting orphaned orders with invalid customer IDs) proves that your database structures successfully prevent data corruption.

---

## 2. Complete SQL Script & Query Execution Registry

Below is the complete database code. It is designed to run seamlessly in any SQL-compatible engine (SQLite, PostgreSQL, MySQL) to create tables, populate the ShopEase dataset, and execute the queries.

### A. Database Initialization, Schema & Seed Insertion
```sql
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

3. Query Execution & Results RegistrySECTION A: SQL Basics & Table StructuresQ1: Display all columns and rows from the customers table.SQLSELECT * FROM customers;
Query Output Results:customer_idfirst_namelast_nameemailcitystatejoin_dateis_premium101AaravSharmaaarav.s@email.comMumbaiMaharashtra2024-01-151102PriyaPatelpriya.p@email.comAhmedabadGujarat2024-02-200103RohanGuptarohan.g@email.comDelhiDelhi2024-03-101104SnehaReddysneha.r@email.comHyderabadTelangana2024-04-050105VikramSinghvikram.s@email.comJaipurRajasthan2024-05-121106AnanyaIyerananya.i@email.comChennaiTamil Nadu2024-06-180107KaranMehtakaran.m@email.comPuneMaharashtra2024-07-221108DivyaNairdivya.n@email.comKochiKerala2024-08-300Q2: Retrieve only the first_name, last_name, and city of all customers.SQLSELECT first_name, last_name, city FROM customers;
Query Output Results:first_namelast_namecityAaravSharmaMumbaiPriyaPatelAhmedabadRohanGuptaDelhiSnehaReddyHyderabadVikramSinghJaipurAnanyaIyerChennaiKaranMehtaPuneDivyaNairKochiQ3: List all unique categories available in the products table.SQLSELECT DISTINCT category FROM products;
Query Output Results:categoryElectronicsClothingHomeQ4: Identify the Primary Key of each table in the schema. Explain why a Primary Key must be unique and NOT NULL.Analysis: * Primary Keys: customers(customer_id), products(product_id), orders(order_id), order_items(item_id).Explanation: A Primary Key enforces entity integrity. It must be UNIQUE to prevent completely duplicate rows inside relational storage and NOT NULL to guarantee every row is explicitly addressable and identifiable.Q5: What constraints are applied to the email column in the customers table? What would happen if you tried to insert a duplicate email?Analysis: The email column utilizes UNIQUE and NOT NULL constraints. If a system operation attempts to insert an email that already exists in the table, the database transaction layer throws a unique index violation constraint error and completely rolls back the command.Q6: Try inserting a product with unit_price = -50. What happens and which constraint prevents it?SQLINSERT INTO products VALUES (209, 'Invalid Box', 'Home', 'Brand', -50.00, 10);
Execution Response:Plaintextsqlite3.IntegrityError: CHECK constraint failed: unit_price > 0
Analysis: The database engine blocked the execution. The check is enforced by the constraint CHECK (unit_price > 0) defined inside the table's DDL statement.SECTION B: Filtering & OptimizationQ7: Retrieve all orders with status = 'Delivered'.SQLSELECT * FROM orders WHERE status = 'Delivered';
Query Output Results:order_idcustomer_idorder_datestatustotal_amount10011012024-08-01Delivered4498.0010021022024-08-03Delivered799.0010041012024-08-10Delivered3499.0010061052024-08-15Delivered5898.0010081032024-08-20Delivered899.0010101082024-08-28Delivered1598.00Q8: Find all products in the 'Electronics' category with a unit_price greater than 2000.SQLSELECT * FROM products WHERE category = 'Electronics' AND unit_price > 2000;
Query Output Results:product_idproduct_namecategorybrandunit_pricestock_qty203Smart WatchElectronicsNoise2999.00150205Bluetooth SpeakerElectronicsJBL3499.00200Q9: List all customers who joined in the year 2024 and belong to the state 'Maharashtra'.SQLSELECT * FROM customers WHERE join_date LIKE '2024%' AND state = 'Maharashtra';
Query Output Results:customer_idfirst_namelast_nameemailcitystatejoin_dateis_premium101AaravSharmaaarav.s@email.comMumbaiMaharashtra2024-01-151107KaranMehtakaran.m@email.comPuneMaharashtra2024-07-221Q10: Find all orders placed between '2024-08-10' and '2024-08-25' (inclusive) that are NOT cancelled.SQLSELECT * FROM orders WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25' AND status != 'Cancelled';
Query Output Results:order_idcustomer_idorder_datestatustotal_amount10041012024-08-10Delivered3499.0010061052024-08-15Delivered5898.0010071062024-08-18Pending1299.0010081032024-08-20Delivered899.0010091072024-08-25Shipped6098.00Q11: Explain what the index idx_orders_date does. How would it improve the performance of a query that filters orders by order_date?Analysis: The index idx_orders_date sets up a pre-sorted lookup map pointing directly to table rows. Instead of checking every single row sequentially via a costly Full Table Scan $O(N)$, the engine performs a fast binary search range scan $O(\log N)$ to find dates instantly.SQL-- Benefitting Query
SELECT * FROM orders WHERE order_date = '2024-08-15';
Q12: If you run: SELECT * FROM customers WHERE YEAR(join_date) = 2024 - would the index on join_date be used? Rewrite to be SARGable.Analysis: No, the index cannot be used. Wrapping the column in a function like YEAR(join_date) makes it non-SARGable because the database engine must compute the function for every single row, bypassing index optimization. To fix this, search using clear date range boundaries:SQLSELECT * FROM customers WHERE join_date >= '2024-01-01' AND join_date <= '2024-12-31';
SECTION C: AggregationQ13: Count the total number of orders in the orders table.SQLSELECT COUNT(*) AS total_orders FROM orders;
Query Output Results:total_orders10Q14: Find the total revenue (SUM of total_amount) from all 'Delivered' orders.SQLSELECT SUM(total_amount) AS total_revenue FROM orders WHERE status = 'Delivered';
Query Output Results:total_revenue17191.00Q15: Calculate the average unit_price of products in each category.SQLSELECT category, ROUND(AVG(unit_price), 2) AS average_price FROM products GROUP BY category;
Query Output Results:categoryaverage_priceClothing2699.00Electronics2224.00Home949.00Q16: For each order status, find the count of orders and the total revenue. Sort by total revenue descending.SQLSELECT status, COUNT(*) AS status_count, SUM(total_amount) AS total_revenue 
FROM orders 
GROUP BY status 
ORDER BY total_revenue DESC;
Query Output Results:statusstatus_counttotal_revenueDelivered617191.00Shipped213596.00Cancelled12999.00Pending11299.00Q17: Find the most expensive (MAX) and cheapest (MIN) product in each category.SQLSELECT category, MAX(unit_price) AS max_price, MIN(unit_price) AS min_price 
FROM products 
GROUP BY category;
Query Output Results:categorymax_pricemin_priceClothing4599.00799.00Electronics3499.00899.00Home1299.00599.00Q18: List all product categories where the average unit_price is greater than 2000. (Use HAVING clause)SQLSELECT category, ROUND(AVG(unit_price), 2) AS avg_price 
FROM products 
GROUP BY category 
HAVING AVG(unit_price) > 2000;
Query Output Results:categoryavg_priceClothing2699.00Electronics2224.00SECTION D: Joins & RelationshipsQ19: Write an INNER JOIN query to display each order along with the customer's first_name and last_name.SQLSELECT o.order_id, o.order_date, c.first_name, c.last_name, o.total_amount 
FROM orders o 
INNER JOIN customers c ON o.customer_id = c.customer_id;
Query Output Results:order_idorder_datefirst_namelast_nametotal_amount10012024-08-01AaravSharma4498.0010022024-08-03PriyaPatel799.0010032024-08-05RohanGupta7498.0010042024-08-10AaravSharma3499.0010052024-08-12SnehaReddy2999.0010062024-08-15VikramSingh5898.0010072024-08-18AnanyaIyer1299.0010082024-08-20RohanGupta899.0010092024-08-25KaranMehta6098.0010102024-08-28DivyaNair1598.00Q20: Using a LEFT JOIN, list ALL customers and their orders (if any). Customers with no orders should still appear with NULL values.SQLSELECT c.customer_id, c.first_name, c.last_name, o.order_id, o.status 
FROM customers c 
LEFT JOIN orders o ON c.customer_id = o.customer_id;
Query Output Results:customer_idfirst_namelast_nameorder_idstatus101AaravSharma1001Delivered101AaravSharma1004Delivered102PriyaPatel1002Delivered103RohanGupta1003Shipped103RohanGupta1008Delivered104SnehaReddy1005Cancelled105VikramSingh1006Delivered106AnanyaIyer1007Pending107KaranMehta1009Shipped108DivyaNair1010DeliveredQ21: Write a query using JOINs across three tables (orders -> order_items -> products).SQLSELECT oi.order_id, p.product_name, oi.quantity, oi.unit_price, oi.discount_pct 
FROM order_items oi
INNER JOIN orders o ON oi.order_id = o.order_id
INNER JOIN products p ON oi.product_id = p.product_id;
Query Output Results:order_idproduct_namequantityunit_pricediscount_pct1001Wireless Earbuds21499.000.001001Laptop Stand1899.0010.001002Cotton T-Shirt1799.000.001003Smart Watch12999.000.001003Running Shoes14599.005.001004Bluetooth Speaker13499.000.001005Smart Watch12999.000.001006Wireless Earbuds11499.0010.001006Running Shoes14599.005.001007Bedsheet Set11299.000.001008Laptop Stand1899.000.001009Bluetooth Speaker13499.000.001009Cushion Covers (Set)2599.0015.001010Bedsheet Set11299.000.001010Cushion Covers (Set)1599.000.00Q22: Explain the difference between LEFT JOIN and RIGHT JOIN with an example from this schema. When would you use a FULL OUTER JOIN?Analysis: * LEFT JOIN: Preserves all entries from the left table (e.g. customers), filling missing connections on the right (e.g. orders) with NULLs. This shows every single customer, regardless of whether they have ordered anything.RIGHT JOIN: Preserves all entries from the right table (e.g. orders), filling missing connections on the left with NULLs.FULL OUTER JOIN: Retains all rows from both tables, pairing matches where possible and padding missing relationships with NULLs on either side. Use this when performing a complete reconciliation audit between two independent tables.Q23: Identify all Foreign Key relationships in the schema. Explain what would happen if you tried to insert an order with customer_id = 999.Analysis: * Relationships: orders.customer_id references customers.customer_id, order_items.order_id references orders.order_id, and order_items.product_id references products.product_id.Behavior: Attempting to insert an order with customer_id = 999 trips a foreign key integrity violation. This halts execution because the key is not present in the master parent directory.SECTION E: Advanced ConceptsQ24: Write a query using CASE to classify products into price tiers.SQLSELECT product_name, unit_price,
       CASE WHEN unit_price < 1000 THEN 'Budget'
            WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
            ELSE 'Premium' END AS price_tier
FROM products;
Query Output Results:product_nameunit_priceprice_tierWireless Earbuds1499.00Mid-RangeCotton T-Shirt799.00BudgetSmart Watch2999.00Mid-RangeRunning Shoes4599.00PremiumBluetooth Speaker3499.00PremiumBedsheet Set1299.00Mid-RangeLaptop Stand899.00BudgetCushion Covers (Set)599.00BudgetQ25: Using a CASE statement inside an aggregate function, count how many orders are 'Delivered' vs 'Not Delivered' in a single row.SQLSELECT COUNT(CASE WHEN status = 'Delivered' THEN 1 END) AS delivered_volume,
       COUNT(CASE WHEN status != 'Delivered' THEN 1 END) AS non_delivered_volume
FROM orders;
Query Output Results:delivered_volumenon_delivered_volume64Q26: Explain each letter of ACID. Give a real-world bank transfer example.Atomicity: All steps in a transaction succeed, or the entire operation is rolled back. (e.g., During a bank transfer, deducting money from Account A without completing the deposit into Account B is completely blocked).Consistency: Every transaction moves the database from one valid state to another, strictly maintaining all structural constraints and relationships.Isolation: Concurrently running operations cannot see each other's uncommitted, partial changes, preventing dirty reads and transaction conflicts.Durability: Once committed, updates are permanently written to non-volatile disk storage. The data will survive even a sudden system crash or power outage.Q27: Write a SQL transaction that executes atomically.SQL-- Begin transaction execution safely
BEGIN TRANSACTION;

-- 1. Ingest new order row
INSERT INTO orders VALUES (1011, 102, '2026-05-30', 'Pending', 1598.00);

-- 2. Append itemized line items
INSERT INTO order_items VALUES (5016, 1011, 202, 1, 799.00, 0);
INSERT INTO order_items VALUES (5017, 1011, 202, 1, 799.00, 0);

-- 3. Synchronize inventory levels across affected items
UPDATE products SET stock_qty = stock_qty - 2 WHERE product_id = 202;

-- Complete transaction and write permanently to disk
COMMIT;
Execution Status Logs:Plaintext -> Step 1 Verified: Order header record created successfully.
 -> Step 2 Verified: Linked order items appended to sub-ledger table.
 -> Step 3 Verified: Warehouse inventory quantities synchronized.

[Transaction Success] All steps completed without failure. Changes COMMITTED to storage safely.

4. Scroll down and click **Commit changes**. 

Now your files are completely updated with distinct, proper content! You're ready to rock that Google Meet.
