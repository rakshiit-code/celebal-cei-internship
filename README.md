# Celebal Technologies: Data Science & Analytics Internship Portfolio

An enterprise-grade repository tracking the 8-week data science and database engineering training modules, pipelines, and project portfolio.

## Project Directory
* **Module 1 (Week 1):** Enterprise E-Commerce Data Exploration & Automated Cleansing Pipeline
* **Module 2 (Week 2):** Relational Database Architecture & Advanced SQL Business Intelligence Portfolio

---

## Module 1: Enterprise E-Commerce Data Exploration & Cleansing
* **Core Toolkit:** Python, Pandas, NumPy, Glob, OS Virtual Layer
* **Dataset Target:** Multiclass Shopping Purchase Ledger (99 Consolidations)

### Key Engineering Implementation Matrix
1. **Automated Ingestion Pipeline:** Programmatically targeted and consolidated 99 individual split file parts from the raw storage layer into a unified dataframe footprint.
2. **Data Sanitization Operations:** Dropped transactional duplicates and filled missing attributes using column-specific medians and categorical modes to preserve database completeness.
3. **Feature Derivation:** Implemented vectorized matrix multiplication to construct a clean, operational `total_amount` metric ($Total = Unit Price \times Quantity$).
4. **Deliverables:** Completed interactive Jupyter logic notebook (`Data_Cleaning_Module_1.ipynb`) alongside the verified dataset artifact (`cleaned_shopping_dataset.csv`).

---

## Module 2: Relational Database Architecture & SQL Analytics
* **Core Toolkit:** SQL, SQLite3, Relational Schemas, Indexing, Transaction Engine
* **Dataset Target:** ShopEase Relational DBMS (Customers, Products, Orders, Order Items)

### Key Analytical & Engineering Implementation Matrix
1. **Relational Schema Definition:** Engineered tables with strict integrity constraints, including `PRIMARY KEY`, `FOREIGN KEY` cascades, `UNIQUE` rules, and numeric domain `CHECK` bounds.
2. **Query Performance Optimization:** Constructed non-clustered B-Tree indices and modified structural conditions to be fully SARGable, shifting filters from costly $O(N)$ table scans to high-performance $O(\log N)$ range scans.
3. **Multi-Dimensional Aggregations:** Formulated advanced analytical group functions, combining conditional `HAVING` filters with cumulative calculations to isolate high-value revenue sectors.
4. **Multi-Table Join Operations:** Linked deep relational models using nested `INNER JOIN` and `LEFT JOIN` layouts to construct full customer transactional history tables.
5. **ACID Compliance & Atomic Transactions:** Implemented a secure, multi-statement SQL transaction sequence with built-in rollback recovery mechanics to guarantee inventory synchronization safety.
6. **Deliverables:** Highly detailed relational querying notebook (`SQL_ECommerce_Analytics_Module_2.ipynb`) showing complete schema designs, verified execution printouts, and ACID compliance logs.
