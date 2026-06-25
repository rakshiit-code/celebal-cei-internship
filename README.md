# Celebal Technologies: Data Engineering Portfolio

![Project Status](https://img.shields.io/badge/Internship_Portfolio-Active-blue?style=for-the-badge)
![Database Engine](https://img.shields.io/badge/DBMS-SQLite3%20%7C%20PostgreSQL-emerald?style=for-the-badge)
![Pipeline Stack](https://img.shields.io/badge/Pipeline-Python%20%7C%20Pandas-orange?style=for-the-badge)

An enterprise-grade repository tracking core milestones, complex processing pipelines, relational database engines, and structural querying assets managed over the 8-week corporate training program.

---

## 📂 Repository Blueprint & Deliverables Map

| Portfolio Phase | Focus Domain | Primary Deliverables |
| :--- | :--- | :--- |
| **Module 1 (Week 1)** | Core Data Engineering & Automation | Automated File Ingestion & Imputation Pipeline |
| **Module 2 (Week 2)** | Relational DB Engineering | Schema Architecture, Query Optimization & Transactions | 
| **Module 3 (Week 3)** | Advanced Analytical Engine | 3NF Schema, Subqueries, CTEs, & Window Functions | 
| **Module 4 (Week 4)** | Cloud Data Orchestration | Azure ADF Pipelines & Blob Storage Integration |
| **Module 5 (Week 5)** | Big Data & Distributed Computing | PySpark Pipelines, Shuffling & In-Memory Analytics |


---

## 🛠️ Week 1: Automated Data Cleansing & Ingestion Pipeline
* **Core Technology Stack:** Python 3.x | Pandas | NumPy | Glob Engine
* **Target Analytical Footprint:** Multiclass Shopping Purchase Ledger (99 Consolidating Split File Artifacts)

### Key Engineering Architecture
* **High-Volume Data Aggregation:** Programmatically scanned, matched, and consolidated 99 separate CSV file parts into a single integrated dataframe footprint.
* **Database Imputation Strategy:** Eliminated data anomalies by filtering duplicate records, applying numerical medians to fill missing value arrays, and implementing categorical modes to repair text properties.

---

## 🛠️ Week 2: Relational Schema Design & Business Intelligence Analytics
* **Core Technology Stack:** Structured Query Language (SQL) | SQLite3 Engine | Indexing Optimization Models
* **Target Enterprise System:** ShopEase Relational DBMS (Customers, Products, Orders, Order_Items Schemas)

### Key Database Implementations
* **Referential Schema Enforcement:** Modeled multiple tables with robust field constraints, utilizing strict PRIMARY KEY mappings, operational FOREIGN KEY cascades, and entity-level UNIQUE validations.
* **Multi-Dimensional Analytical Queries:** Constructed deep multi-table aggregates using nested INNER JOIN and LEFT JOIN operations to compile absolute customer lifecycle value trends.

---

## 🛠️ Week 3: Advanced Relational Analytical Engine & Superstore Mining
* **Core Technology Stack:** SQL | Python | Pandas | SQLite3 Engine | Advanced Window Functions
* **Target Enterprise System:** Superstore Relational Analytics (Customers, Products, Orders Normalized Schemas)

### Key Engineering & Analytical Architecture
* **Relational Schema Normalization:** Decoupled unstructured raw datasets into a clean, normalized 3NF relational architecture (Customers, Products, Orders) using efficient SELECT DISTINCT routines.
* **Complex Data Mining Engine:** Engineered enterprise-grade data structures by implementing:
    * **Nested Subqueries & CTEs:** Orchestrated multi-layer data transformations to isolate peak revenue contributors and calculate global financial averages.
    * **Analytical Window Functions:** Deployed RANK(), DENSE_RANK(), and ROW_NUMBER() to perform high-precision customer segmentation and sequential transaction tracking.
* **Targeted Business Case Study:** Solved for critical business KPIs, including retention risk analysis, single-order attrition, and high-value cart order tracking, delivering actionable insights.

---
## 🛠️ Week 4: Cloud Data Orchestration & Azure Pipeline Integration
* **Core Technology Stack:** Azure Data Factory (ADF) | Azure Blob Storage | IAM (RBAC)
* **Target Enterprise System:** End-to-End Cloud Data Pipeline

### Key Engineering & Analytical Architecture
* **Cloud Resource Architecture:** Provisioned secure, scalable infrastructure including Resource Groups, Storage Accounts, and Data Factory instances within Azure.
* **Orchestration Workflow:** Designed and executed a robust data pipeline utilizing **Get Metadata** for file validation and **Copy Data** activities for seamless transfer from raw storage to processed sinks.
* **Security & Governance:** Implemented granular IAM/RBAC controls to ensure secure access to Azure resources, adhering to enterprise security standards.
* **Performance Monitoring:** Configured pipeline triggers and debug sessions to monitor activity duration, throughput, and execution success, ensuring high availability and reliability of data flows.
*End of Portfolio | Verified Stable | Author: Rakshit Gupta*
---

## 🛠️ Week 5: Distributed Big Data Processing with PySpark
* **Core Technology Stack:** Apache Spark | PySpark | DAG Execution | Wide Transformations
* **Target Enterprise System:** Scalable Distributed Analytical Pipeline

### Key Engineering & Analytical Architecture
* **In-Memory Computing Transition:** Migrated data processing workflows from disk-based MapReduce patterns to Spark’s high-performance in-memory engine, significantly reducing iterative processing latency.
* **Distributed Transformation Engine:** Engineered complex analytical pipelines utilizing both **Narrow** and **Wide transformations**; effectively managed shuffle partitions and DAG scheduling to optimize data redistribution across cluster nodes.
* **Production-Grade Data Cleansing:** Implemented robust PySpark routines for automated schema enforcement, null/missing value imputation, and type-safe casting (e.g., `TimestampType` conversion) to ensure high-fidelity data downstream.
* **Advanced Aggregation Logic:** Constructed scalable aggregation engines using PySpark SQL functions (`count`, `sum`, `avg`, `min`, `max`) combined with conditional `groupBy` operations to derive enterprise-level KPIs from massive datasets.
* **Performance Analysis:** Conducted detailed observations on shuffle overhead and compute performance, providing technical insights into cluster resource utilization and DAG execution efficiency.

> **Technical Artifacts:** Includes comprehensive Q&A (Q1–Q15) covering Spark architecture, session management, and real-time output validation.
