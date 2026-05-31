# Celebal Technologies: Data Science & Analytics Portfolio

![Project Status](https://img.shields.io/badge/Internship_Portfolio-Active-blue?style=for-the-badge)
![Database Engine](https://img.shields.io/badge/DBMS-SQLite3%20%7C%20PostgreSQL-emerald?style=for-the-badge)
![Pipeline Stack](https://img.shields.io/badge/Pipeline-Python%20%7C%20Pandas-orange?style=for-the-badge)

An enterprise-grade repository tracking core milestones, complex processing pipelines, relational database engines, and structural querying assets managed over the 8-week corporate training program.

---

## 📂 Repository Blueprint & Deliverables Map

| Portfolio Phase | Focus Domain | Primary Deliverables | Reference Assets |
| :--- | :--- | :--- | :--- |
| **Module 1 (Week 1)** | Core Data Engineering & Automation | Automated File Ingestion & Imputation Pipeline | 📝 [Data_Cleaning_Module_1.ipynb](./Week_1/Data_Cleaning_Module_1.ipynb) |
| **Module 2 (Week 2)** | Relational DB Engineering | Schema Architecture, Query Optimization & Transactions | 📝 [SQL_ECommerce_Analytics_Module_2.ipynb](./Week_2/SQL_ECommerce_Analytics_Module_2.ipynb) |
| **Executive Summary** | Business Intelligence Insights | Production Analytics & Structural Performance Ledger | 📑 [Module 2 Full Submission Report](./Week_2/Module_2_Submission_Report.md) |

---

## 🛠️ Week 1: Automated Data Cleansing & Ingestion Pipeline
* **Core Technology Stack:** `Python 3.x` | `Pandas` | `NumPy` | `Glob Engine` | `OS Virtualization Layer`
* **Target Analytical Footprint:** Multiclass Shopping Purchase Ledger (99 Consolidating Split File Artifacts)

### Key Engineering Architecture
* **High-Volume Data Aggregation:** Programmatically scanned, matched, and consolidated 99 separate CSV file parts scattered across raw storage layers into a single integrated dataframe footprint using Python's `glob` system.
* **Database Imputation Strategy:** Eliminated data anomalies by filtering duplicate records, applying calculated numerical column medians to fill missing value arrays, and implementing categorical modes to repair text properties without shifting semantic distributions.
* **Vectorized Matrix Operations:** Wrote optimized Python code to compute missing transaction summaries, deriving a clean, true transaction value array based on the formula:
  $$Total\_Amount = Unit\_Price \times Quantity$$

> **Data Engineering Artifacts Directory:**
> * Interactive Notebook Execution File: [`./Week_1/Data_Cleaning_Module_1.ipynb`](./Week_1/Data_Cleaning_Module_1.ipynb)
> * Production Dataset Release: [`./Week_1/cleaned_shopping_dataset.csv`](./Week_1/cleaned_shopping_dataset.csv)

---

## 🛠️ Week 2: Relational Schema Design & Business Intelligence Analytics
* **Core Technology Stack:** `Structured Query Language (SQL)` | `SQLite3 Engine` | `Indexing Optimization Models`
* **Target Enterprise System:** ShopEase Relational DBMS (`Customers`, `Products`, `Orders`, `Order_Items` Schemas)

### Key Database Implementations
* **Referential Schema Enforcement:** Modeled multiple tables with robust field constraints, utilizing strict `PRIMARY KEY` mappings, operational `FOREIGN KEY` cascades, entity-level `UNIQUE` validations, and protective numerical domain `CHECK` rules.
* **Query Performance Tuning:** Examined execution maps to build optimized index lookups. Rewrote slow query code blocks into fully **SARGable format**, shifting index performance from slow, full table linear scans ($O(N)$ complexity) into high-efficiency tree range lookups ($O(\log N)$ latency complexity).
* **Multi-Dimensional Analytical Queries:** Constructed deep multi-table aggregates using nested `INNER JOIN` and `LEFT JOIN` operations to compile absolute customer lifecycle value trends across Indian markets.
* **ACID Transactions Security:** Programmed a fault-tolerant multi-step operational script wrapped inside transactional safety handles (`BEGIN TRANSACTION` $\rightarrow$ `COMMIT / ROLLBACK`), ensuring inventory stock coordinates sync atomically whenever a customer purchase is logged.

> **Relational Engineering Assets Directory:**
> * Full Analytical Querying Notebook: [`./Week_2/SQL_ECommerce_Analytics_Module_2.ipynb`](./Week_2/SQL_ECommerce_Analytics_Module_2.ipynb)
> * Executive Business Intelligence Report: [`./Week_2/Module_2_Submission_Report.md`](./Week_2/Module_2_Submission_Report.md)

---
*Developed during the Celebal Technologies Data Science & Analytics Internship. Managed and mainlined under the `rakshiit-code` production repository.*
