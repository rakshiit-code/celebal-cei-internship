# Azure Cloud Fundamentals & Data Pipeline using ADF

**Week's Assignment** — Azure Data Factory | Blob Storage | IAM | Pipelines

---

##  Objective

Understand core Azure cloud concepts and build a complete, end-to-end data pipeline using **Azure Storage Account** and **Azure Data Factory (ADF)**.

---

##  Assignment Structure

| Task | Title | Key Activities | Deliverable |
|------|-------|---------------|-------------|
| Task 1 | Azure Portal Exploration | Resource Group creation | Screenshot |
| Task 2 | Storage Setup | Storage Account, Blob Container, CSV upload | Screenshot |
| Task 3 | ADF Basics | Linked Service, Datasets, Get Metadata | 3 Screenshots |
| Task 4 | Pipeline Development | Copy Data activity, source/sink config | Screenshot |
| Task 5 | Pipeline Execution | Debug/Trigger run, monitor results | Screenshot |
| Task 6 | IAM Roles | Reader, Contributor, ADF Storage access | Screenshot |
| 🏁 Mini Project | Complete Pipeline | End-to-end CSV pipeline with metadata check | Full Submission |

---

##  Tasks

### Task 1 — Azure Portal Exploration
- Explored the Azure Portal layout (Dashboard, Search, All Services)
- Created a **Resource Group**: `rg-week4`
- Subscription: **Azure for Students**
- Region: **East US**

**Deliverable:** Screenshot of the created Resource Group

---

### Task 2 — Storage Setup
- Created an **Azure Storage Account**: `stweek4rakshit438`
- Created a **Blob Container**: `raw-data` (Access key authentication)
- Uploaded dataset: `Sample - Superstore....` (2.18 MiB, Block blob)

**Deliverable:** Screenshot of `raw-data` container with uploaded Superstore CSV file

---

### Task 3 — ADF Basics
- Created **Azure Data Factory** instance: `adfweek4rakshit4388`
- Explored ADF Studio: Author / Monitor / Manage tabs
- Created **Linked Service**: `AzureBlobStorage_linked` (Type: Azure Blob Storage ✅)
- Created **Source Dataset**: `DS_Source_CSV`
  - Linked Service: `AzureBlobStorage_linked`
  - File path: `raw-data / Sample - Superstore....`
  - Format: DelimitedText (CSV), Comma delimiter, UTF-8
- Used **Get Metadata** activity (`Get Metadata1`) on `pipeline1`
  - Status: ✅ Succeeded

**Deliverables:**
- Screenshot of Linked Service (`AzureBlobStorage_linked`)
- Screenshot of Dataset (`DS_Source_CSV`) configuration
- Screenshot of Get Metadata activity output (Succeeded)

---

### Task 4 — Pipeline Development
- Created pipeline: `PL_Copy_EmployeeData`
- Added **Copy Data** activity: `pl_Copy_sample-superstore data`
- Source: `DS_Source_CSV` (Superstore CSV from `raw-data/`)
- Sink: destination in Blob Storage

**Deliverable:** Screenshot of pipeline canvas with Copy Data activity

---

### Task 5 — Pipeline Execution
- Ran the pipeline using **Debug** mode
- Activity: `pl_Copy_sample-superstore dat` — ✅ **Succeeded**

**Copy Details:**
| Metric | Value |
|--------|-------|
| Data read | 2.288 MB |
| Data written | 2.288 MB |
| Files read | 1 |
| Files written | 1 |
| Rows skipped | 0 |
| Throughput | 1.144 MB/s |
| Copy duration | 00:00:10 |
| Used DIUs | 4 |

**Deliverable:** Screenshot showing pipeline **Succeeded** status and copy activity details

---

### Task 6 — IAM Roles
IAM configured on Resource Group: `rg-week4`

| Role | User | Type | Scope |
|------|------|------|-------|
| Owner | Rakshit Gupta | User | Subscription (Inherited) |
| Owner | Rakshit Gupta | User | Subscription (Inherited) |
| Reader | Rakshit Gupta | User | This resource |
| Backup Contributor | Rakshit Gupta | User | This resource |
| Workbook Contributor | Rakshit Gupta | User | This resource |

Total: **5 role assignments** (3 Job function roles, 2 Privileged administrator roles)

**Deliverable:** Screenshot of Access Control (IAM) showing all role assignments

---

## 🏁 Mini Project — End-to-End Pipeline

### Problem Statement
Build a complete pipeline that reads the Sample Superstore CSV from Blob Storage, validates its metadata, and copies the data to a new destination location.

### Architecture
---

##  Azure Resources Used

| Resource | Actual Name | Purpose |
|----------|-------------|---------|
| Resource Group | `rg-week4` | Container for all resources |
| Storage Account | `stweek4rakshit438` | Blob storage for CSV files |
| Blob Container | `raw-data` | Input file storage |
| Source File | `Sample - Superstore....csv` (2.18 MiB) | Dataset for pipeline |
| Azure Data Factory | `adfweek4rakshit4388` | Pipeline orchestration |
| Linked Service | `AzureBlobStorage_linked` | ADF ↔ Storage connection |
| Source Dataset | `DS_Source_CSV` | Points to Superstore CSV in `raw-data/` |
| Pipeline | `PL_Copy_EmployeeData` | Copy + Metadata pipeline |
| Pipeline Activity | `pl_Copy_sample-superstore data` | Copy Data activity |

---

##  Key Concepts Covered

- **Resource Group** — Logical container for Azure resources
- **Blob Storage** — Unstructured data storage (CSV, JSON, images, etc.)
- **Linked Service** — Connection definition in ADF
- **Dataset** — Pointer to a specific data location/format
- **Copy Data Activity** — Moves data from source to sink
- **Get Metadata Activity** — Retrieves file properties for validation
- **IAM / RBAC** — Role-based access control for Azure resources
- **Integration Runtime** — Compute infrastructure used by ADF to run activities
