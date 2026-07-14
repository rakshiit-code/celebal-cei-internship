# Databricks notebook source
# MAGIC %md
# MAGIC # Project Sentinel — Step 2: Landing to Bronze
# MAGIC
# MAGIC Moves data from Landing into the Bronze layer as structured Delta. The original,
# MAGIC messy payload is preserved untouched — Bronze only *adds* simple metadata
# MAGIC (ingestion lineage, a stable surrogate key, a load batch id). No cleansing happens
# MAGIC here; that's Silver's job.

# COMMAND ----------

dbutils.widgets.text("catalog", "sentinel_catalog", "Unity Catalog Catalog")
dbutils.widgets.text("schema", "sentinel", "Schema")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

landing_table = f"{catalog}.{schema}.landing_upi_transactions"
bronze_table = f"{catalog}.{schema}.bronze_upi_transactions"

# COMMAND ----------

from pyspark.sql import functions as F

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {bronze_table} (
    bronze_id            STRING,
    transaction_id       STRING,
    timestamp            STRING,
    sender_vpa           STRING,
    receiver_vpa         STRING,
    amount               STRING,
    currency             STRING,
    status               STRING,
    device_id            STRING,
    ip_address           STRING,
    transaction_type     STRING,
    bank_ref_no          STRING,
    sender_mobile        STRING,
    receiver_mobile      STRING,
    is_fraud_seed        BOOLEAN,
    _source_file          STRING,
    _ingest_timestamp      TIMESTAMP,
    _bronze_load_timestamp TIMESTAMP,
    _bronze_batch_id        STRING
)
USING DELTA
""")

# COMMAND ----------

# MAGIC %md ### Incremental read of Landing → append-only write to Bronze
# MAGIC
# MAGIC Uses a Delta merge on `transaction_id` so re-running this notebook is idempotent —
# MAGIC re-ingesting the same landing rows will not create duplicate Bronze rows.

# COMMAND ----------

from delta.tables import DeltaTable
import uuid

batch_id = str(uuid.uuid4())

landing_df = spark.table(landing_table)

bronze_batch_df = (
    landing_df
    .withColumn("bronze_id", F.expr("uuid()"))
    .withColumn("_bronze_load_timestamp", F.current_timestamp())
    .withColumn("_bronze_batch_id", F.lit(batch_id))
)

bronze_tbl = DeltaTable.forName(spark, bronze_table)

(
    bronze_tbl.alias("tgt")
    .merge(
        bronze_batch_df.alias("src"),
        "tgt.transaction_id = src.transaction_id"
    )
    .whenNotMatchedInsertAll()
    .execute()
)

# COMMAND ----------

# MAGIC %md ### Sanity check

# COMMAND ----------

count = spark.table(bronze_table).count()
print(f"Bronze table {bronze_table} now has {count} rows.")
display(spark.table(bronze_table).limit(10))

# COMMAND ----------

dbutils.notebook.exit(f"bronze_table={bronze_table};row_count={count}")
