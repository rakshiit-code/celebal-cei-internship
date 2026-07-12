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
| **Module 6 (Week 6)** | Lakehouse Architecture & Delta Lake | Delta Tables, ACID Compliance, Time Travel & Schema Evolution |
| **Module 7 (Week 7)** | Cloud Data Warehousing & Modern ELT | Snowflake/Synapse Architecture, Advanced Querying & Modeling |
| **Module 8 (Week 8)** | Capstone Architecture & Workflow Orchestration | End-to-End Data Pipeline Integration, Automation & Analytics |

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

---

## 🛠️ Week 6: Next-Generation Lakehouse Architecture with Delta Lake
* **Core Technology Stack:** Databricks | Delta Lake | Apache Spark SQL | Parquet Storage
* **Target Enterprise System:** ACID-Compliant Transactional Storage Layer

### Key Engineering & Analytical Architecture
* **Lakehouse Table Convergence:** Converted legacy Parquet data lakes into high-performance Delta tables, enabling ACID transaction guarantees over distributed object storage.
* **Time Travel & Auditing Implementation:** Leveraged Delta Lake's historical transaction log (`_delta_log`) to query historical data snapshots using `AS OF` syntax, ensuring total reproducibility and system auditability.
* **Schema Evolution & Enforcement:** Enforced strict structural boundaries on incoming production streams to prevent data corruption while implementing controlled schema migration configurations for structural updates.
* **Storage Optimization Realization:** Programmatically applied `OPTIMIZE` commands coupled with `Z-ORDER BY` multidimensional clustering to dramatically reduce file fragmentation and accelerate scan speeds for critical query paths.

---

## 🛠️ Week 7: Enterprise Data Warehousing & Modern ELT Paradigms
* **Core Technology Stack:** Snowflake/Cloud DW | Advanced SQL | Data Modeling | Stage & Pipe Automation
* **Target Enterprise System:** Centralized Analytical Cloud Data Warehouse

### Key Engineering & Analytical Architecture
* **Modern Warehouse Architecture:** Developed compute-isolated virtual warehouses configured with multi-cluster auto-scaling rules to efficiently manage varying heavy workloads without resource contention.
* **Automated Raw Storage Ingestion:** Provisioned external stages and storage integration patterns to build seamless copy pipelines (`COPY INTO`) executing semi-structured JSON and CSV parsing natively.
* **Advanced Materialized Views & Optimization:** Built high-performance analytical views and optimized clustering keys to drastically reduce query computing costs on multi-million row transactional datasets.
* **Data Security & Masking Policies:** Implemented RBAC security hierarchies combined with dynamic data masking rules to safeguard sensitive column attributes (PII) at rest and during query execution.

---

## 🛠️ Week 8: End-to-End Capstone Production Pipeline & Workflow Orchestration
* **Core Technology Stack:** Integration Stack (ADF | Databricks | Cloud DW | BI Tooling)
* **Target Enterprise System:** Fully Unified Corporate Insights Platform

### Key Engineering & Analytical Architecture
* **End-to-End Orchestration Blueprint:** Combined multi-week concepts into a single robust operational topology: Raw Landing $\rightarrow$ Azure ADF $\rightarrow$ Databricks/Delta Lake Cleansing $\rightarrow$ Cloud Warehousing Serving Layer.
* **Advanced Workflow Scheduling:** Engineered unified task dependency graphs using automated system triggers, event-driven execution patterns, and error handling notification blocks.
* **Analytical Insights Surface:** Transformed aggregate serving-layer metrics into highly scannable visual business intelligence dashboards mapping out real-time enterprise health and operational velocity.
* **Final Deployment Integrity:** Conducted rigorous system integration testing, validating schema enforcement across all staging points, pipeline exception handling, and performance SLAs.

---
*End of Portfolio | Verified Stable | Author: Rakshit Gupta*
