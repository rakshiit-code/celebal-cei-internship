# Databricks notebook source
# MAGIC %md
# MAGIC # Project Sentinel — Step 1: Raw to Landing (Ingestion)
# MAGIC
# MAGIC Reads the raw JSON files dropped in the Unity Catalog Volume by the generator and
# MAGIC lands them **as-is** — no transformations, no cleansing — into a Landing Delta table.
# MAGIC This table is the immutable source of truth: whatever is wrong with the data stays
# MAGIC wrong here on purpose, so every downstream fix is traceable to a specific layer.

# COMMAND ----------

dbutils.widgets.text("catalog", "sentinel_catalog", "Unity Catalog Catalog")
dbutils.widgets.text("schema", "sentinel", "Schema")
dbutils.widgets.text("volume", "raw_telemetry", "Volume name")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
volume = dbutils.widgets.get("volume")

volume_path = f"/Volumes/{catalog}/{schema}/{volume}"
landing_table = f"{catalog}.{schema}.landing_upi_transactions"
checkpoint_path = f"/Volumes/{catalog}/{schema}/{volume}/_checkpoints/landing"

# COMMAND ----------

# MAGIC %md ### Read raw JSON exactly as it lands
# MAGIC
# MAGIC Everything is read as a string first (`amount` included) so that no implicit type
# MAGIC coercion or silent row-dropping happens on ingest — that job belongs to Silver.

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, StringType, BooleanType

raw_schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("sender_vpa", StringType(), True),
    StructField("receiver_vpa", StringType(), True),
    StructField("amount", StringType(), True),          # kept as string on purpose — see Silver
    StructField("currency", StringType(), True),
    StructField("status", StringType(), True),
    StructField("device_id", StringType(), True),
    StructField("ip_address", StringType(), True),
    StructField("transaction_type", StringType(), True),
    StructField("bank_ref_no", StringType(), True),
    StructField("sender_mobile", StringType(), True),
    StructField("receiver_mobile", StringType(), True),
    StructField("is_fraud_seed", BooleanType(), True),
])

# COMMAND ----------

# MAGIC %md ### Ingest with Auto Loader (streaming, schema-locked, exactly-once)

# COMMAND ----------

from pyspark.sql import functions as F

raw_stream_df = (
    spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", checkpoint_path + "/schema")
    .schema(raw_schema)
    .load(volume_path)
)

landing_df = (
    raw_stream_df
    .withColumn("_source_file", F.input_file_name())
    .withColumn("_ingest_timestamp", F.current_timestamp())
)

# COMMAND ----------

# MAGIC %md ### Write to the Landing Delta table (append-only, immutable)

# COMMAND ----------

query = (
    landing_df.writeStream
    .format("delta")
    .option("checkpointLocation", checkpoint_path)
    .outputMode("append")
    .trigger(availableNow=True)
    .toTable(landing_table)
)

query.awaitTermination()

# COMMAND ----------

# MAGIC %md ### Sanity check

# COMMAND ----------

count = spark.table(landing_table).count()
print(f"Landing table {landing_table} now has {count} rows.")
display(spark.table(landing_table).limit(10))

# COMMAND ----------

dbutils.notebook.exit(f"landing_table={landing_table};row_count={count}")
