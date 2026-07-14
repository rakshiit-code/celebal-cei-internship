# Databricks notebook source
# MAGIC %md
# MAGIC # Project Sentinel — Orchestrator
# MAGIC
# MAGIC Runs the full Medallion pipeline end to end, in order:
# MAGIC
# MAGIC `Generator -> Landing -> Bronze -> Silver -> Gold`
# MAGIC
# MAGIC This can be run interactively, or set as the entry-point notebook of a **Databricks
# MAGIC Workflow (Job)** with a schedule/trigger. Each stage is a separate notebook so it can
# MAGIC also be scheduled independently as multiple Job tasks with dependencies — the chaining
# MAGIC below is the simplest single-notebook version of that same DAG.

# COMMAND ----------

dbutils.widgets.text("catalog", "sentinel_catalog", "Unity Catalog Catalog")
dbutils.widgets.text("schema", "sentinel", "Schema")
dbutils.widgets.text("volume", "raw_telemetry", "Volume name")
dbutils.widgets.text("num_files", "10", "Number of JSON files to generate")
dbutils.widgets.text("records_per_file", "500", "Records per file")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
volume = dbutils.widgets.get("volume")
num_files = dbutils.widgets.get("num_files")
records_per_file = dbutils.widgets.get("records_per_file")

common_params = {"catalog": catalog, "schema": schema}

# COMMAND ----------

# MAGIC %md ### Step 0 — Generate raw telemetry

# COMMAND ----------

result_0 = dbutils.notebook.run(
    "../00_generator/telemetry_generator",
    timeout_seconds=600,
    arguments={**common_params, "volume": volume, "num_files": num_files, "records_per_file": records_per_file},
)
print("Step 0 result:", result_0)

# COMMAND ----------

# MAGIC %md ### Step 1 — Raw to Landing

# COMMAND ----------

result_1 = dbutils.notebook.run(
    "../01_raw_to_landing/01_ingest_raw_to_landing",
    timeout_seconds=600,
    arguments={**common_params, "volume": volume},
)
print("Step 1 result:", result_1)

# COMMAND ----------

# MAGIC %md ### Step 2 — Landing to Bronze

# COMMAND ----------

result_2 = dbutils.notebook.run(
    "../02_landing_to_bronze/02_landing_to_bronze",
    timeout_seconds=600,
    arguments=common_params,
)
print("Step 2 result:", result_2)

# COMMAND ----------

# MAGIC %md ### Step 3 — Bronze to Silver

# COMMAND ----------

result_3 = dbutils.notebook.run(
    "../03_bronze_to_silver/03_bronze_to_silver",
    timeout_seconds=600,
    arguments=common_params,
)
print("Step 3 result:", result_3)

# COMMAND ----------

# MAGIC %md ### Step 4 — Silver to Gold

# COMMAND ----------

result_4 = dbutils.notebook.run(
    "../04_silver_to_gold/04_silver_to_gold",
    timeout_seconds=600,
    arguments=common_params,
)
print("Step 4 result:", result_4)

# COMMAND ----------

# MAGIC %md ### Pipeline complete ✅

# COMMAND ----------

print("Project Sentinel pipeline run complete.")
print(f"Catalog.Schema: {catalog}.{schema}")
print("Gold tables ready: gold_daily_kpis, gold_fraud_flags, gold_fraud_summary")
