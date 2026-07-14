# Project Sentinel

Real-time UPI transaction & fraud detection pipeline — a foundational Medallion
Architecture implementation on Databricks (Unity Catalog + Delta Lake + Auto Loader).

No dataset ships with this project. Everything is generated at run time by
`00_generator/telemetry_generator.py`.

## Pipeline

```
Step 0                Step 1              Step 2              Step 3              Step 4
Generator      -->    Raw to Landing -->  Landing to    -->   Bronze to    -->    Silver to
(Python, UC Volume)   (Auto Loader)       Bronze              Silver              Gold
                                          (Delta, +meta)      (cleanse, mask,     (KPIs + fraud
                                                               quarantine)         scoring)
```

| Layer | Table | What happens |
|---|---|---|
| Raw | Files in `/Volumes/<catalog>/<schema>/raw_telemetry` | Messy JSON, generated |
| Landing | `landing_upi_transactions` | Ingested as-is, `amount` kept as string, immutable |
| Bronze | `bronze_upi_transactions` | + ingestion metadata, idempotent merge on `transaction_id` |
| Silver | `silver_upi_transactions` / `silver_upi_transactions_rejects` | Type-cast, deduped, PII-masked, invalid rows quarantined (not dropped) |
| Gold | `gold_daily_kpis`, `gold_fraud_flags`, `gold_fraud_summary` | Business KPIs + rule-based fraud scoring |

## Folder structure

```
project_sentinel/
├── 00_generator/telemetry_generator.py         # Step 0
├── 01_raw_to_landing/01_ingest_raw_to_landing.py  # Step 1
├── 02_landing_to_bronze/02_landing_to_bronze.py   # Step 2
├── 03_bronze_to_silver/03_bronze_to_silver.py     # Step 3
├── 04_silver_to_gold/04_silver_to_gold.py         # Step 4
├── 05_orchestration/00_main_orchestrator.py       # Runs 0 -> 4 end to end
└── README.md
```

Every file is a Databricks **notebook-source `.py` file** (`# Databricks notebook source`
header + `# COMMAND ----------` cell markers). Import each one individually into a
Databricks Workspace folder (or import the whole folder at once via
Workspace ▸ Import ▸ `.py` file with "Databricks source" format, or the Databricks CLI /
Git folders), and the cell structure, markdown docs, and widgets will all render natively.

## How to run

### Option A — Interactively, one notebook at a time
1. Attach each notebook to a cluster (DBR 13.3 LTS+ recommended, Unity Catalog enabled).
2. Run `00_generator` first — it creates the catalog/schema/volume and drops JSON files.
3. Run `01` → `02` → `03` → `04` in order. Each notebook exposes widgets at the top
   (`catalog`, `schema`, etc.) so you can point every stage at the same place.

### Option B — One click, end to end
Open `05_orchestration/00_main_orchestrator.py` and click **Run All**. It chains all
five notebooks via `dbutils.notebook.run(...)`.

### Option C — Databricks Workflow (recommended for anything beyond a demo)
Create a Job with 5 tasks (Generator → Landing → Bronze → Silver → Gold), each task
pointing at its notebook, with linear `depends_on` edges — this gives you retries,
alerting, and a schedule for free, and mirrors exactly what the orchestrator notebook
does but as first-class, independently-monitorable tasks.

## Key parameters (widgets)

| Widget | Default | Purpose |
|---|---|---|
| `catalog` | `sentinel_catalog` | Unity Catalog catalog name |
| `schema` | `sentinel` | Schema (database) name |
| `volume` | `raw_telemetry` | UC Volume the generator writes into |
| `num_files` | `10` | How many raw JSON files to generate per run |
| `records_per_file` | `500` | Records per generated file |
| `fraud_ratio` | `0.03` | Fraction of records seeded as fraud bursts |
| `corruption_ratio` | `0.15` | Fraction of records seeded with structural corruption |

## Data quality approach

Rather than silently dropping bad rows, Silver **quarantines** them into
`silver_upi_transactions_rejects` with a `_reject_reason` column
(`invalid_amount`, `invalid_timestamp`, `missing_sender_vpa`, etc.), so data quality is
auditable instead of invisible.

## Fraud scoring (Gold)

A simple, explainable rule-based score (0–100) per transaction, combining:
- Amount above the day's 95th percentile (+30)
- Sender made 5+ transactions in a trailing 10-minute window (+30)
- Sender's trailing 10-minute volume exceeds ₹1,00,000 (+25)
- High-value transaction that isn't `SUCCESS` yet (+15)

`fraud_score >= 50` → `HIGH`, `25–49` → `MEDIUM`, else `LOW`.

## Validation

The Bronze/Silver/Gold transformation logic (type casting, quarantine filtering,
dedup window, KPI aggregation, and the fraud-scoring window logic) was unit-tested
locally against a generated sample batch before delivery: 500 raw records →
60 correctly quarantined → 440 clean Silver rows → correct daily KPIs, and every
seeded `fraudster*` transaction was correctly flagged `HIGH` risk.

## Extending this project

- Swap Step 0's file-drop simulation for a real Kafka/Event Hubs source and point
  Auto Loader at it directly — Steps 1-4 don't need to change.
- Replace the rule-based Gold fraud score with a trained model (e.g. an MLflow-logged
  classifier scored via a Pandas UDF) once you have labeled outcomes.
- Add a DLT (Delta Live Tables) pipeline definition to replace Steps 1-4 for automatic
  data quality expectations (`@dlt.expect_or_drop`) and lineage.
