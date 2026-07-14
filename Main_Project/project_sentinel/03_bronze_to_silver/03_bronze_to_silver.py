# Databricks notebook source
# MAGIC %md
# MAGIC # Project Sentinel — Step 3: Bronze to Silver
# MAGIC
# MAGIC This is where the mess gets fixed:
# MAGIC - Cast `amount` to a proper numeric type, tolerating whitespace and string encoding.
# MAGIC - Parse `timestamp` into a real timestamp, dropping unparseable ones.
# MAGIC - Filter out invalid records (nulls in required fields, negative amounts,
# MAGIC   unparseable timestamps).
# MAGIC - Mask PII (`sender_mobile`, `receiver_mobile`) so raw digits never leave Silver.
# MAGIC - Route rejected rows to a `silver_upi_transactions_rejects` quarantine table instead
# MAGIC   of silently dropping them, so data quality is auditable.

# COMMAND ----------

dbutils.widgets.text("catalog", "sentinel_catalog", "Unity Catalog Catalog")
dbutils.widgets.text("schema", "sentinel", "Schema")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

bronze_table = f"{catalog}.{schema}.bronze_upi_transactions"
silver_table = f"{catalog}.{schema}.silver_upi_transactions"
rejects_table = f"{catalog}.{schema}.silver_upi_transactions_rejects"

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

bronze_df = spark.table(bronze_table)

# COMMAND ----------

# MAGIC %md ### Standardize types

# COMMAND ----------

cleaned_df = (
    bronze_df
    # amount: strip whitespace, cast to double (string-encoded numbers become numeric,
    # anything genuinely non-numeric becomes null and gets filtered below)
    .withColumn("amount_clean", F.trim(F.col("amount")).cast(DoubleType()))
    # timestamp: parse the expected format; malformed strings become null
    .withColumn("timestamp_clean", F.to_timestamp("timestamp", "yyyy-MM-dd'T'HH:mm:ss"))
    # mask PII — keep only the last 2 digits for support/debug traceability
    .withColumn(
        "sender_mobile_masked",
        F.when(F.col("sender_mobile").isNotNull(),
               F.concat(F.lit("XXXXXXXX"), F.substring("sender_mobile", -2, 2)))
    )
    .withColumn(
        "receiver_mobile_masked",
        F.when(F.col("receiver_mobile").isNotNull(),
               F.concat(F.lit("XXXXXXXX"), F.substring("receiver_mobile", -2, 2)))
    )
    .withColumn("_silver_load_timestamp", F.current_timestamp())
)

# COMMAND ----------

# MAGIC %md ### Split valid vs. invalid records
# MAGIC
# MAGIC A record is **rejected** if:
# MAGIC - `amount_clean` is null or <= 0 (covers nulls, non-numeric strings, and negative amounts)
# MAGIC - `timestamp_clean` is null (covers nulls and malformed timestamps)
# MAGIC - `sender_vpa` or `receiver_vpa` is null
# MAGIC - `transaction_id` is null (can't dedupe/track a record with no identity)

# COMMAND ----------

is_valid = (
    F.col("amount_clean").isNotNull() & (F.col("amount_clean") > 0)
    & F.col("timestamp_clean").isNotNull()
    & F.col("sender_vpa").isNotNull()
    & F.col("receiver_vpa").isNotNull()
    & F.col("transaction_id").isNotNull()
)

valid_df = cleaned_df.filter(is_valid)
invalid_df = cleaned_df.filter(~is_valid).withColumn(
    "_reject_reason",
    F.concat_ws(
        "; ",
        F.when(F.col("amount_clean").isNull() | (F.col("amount_clean") <= 0), F.lit("invalid_amount")),
        F.when(F.col("timestamp_clean").isNull(), F.lit("invalid_timestamp")),
        F.when(F.col("sender_vpa").isNull(), F.lit("missing_sender_vpa")),
        F.when(F.col("receiver_vpa").isNull(), F.lit("missing_receiver_vpa")),
        F.when(F.col("transaction_id").isNull(), F.lit("missing_transaction_id")),
    )
)

# COMMAND ----------

# MAGIC %md ### Deduplicate valid records (keep latest by ingest time per transaction_id)

# COMMAND ----------

from pyspark.sql.window import Window

w = Window.partitionBy("transaction_id").orderBy(F.col("_bronze_load_timestamp").desc())

silver_final_df = (
    valid_df
    .withColumn("_rn", F.row_number().over(w))
    .filter(F.col("_rn") == 1)
    .drop("_rn", "amount", "timestamp", "sender_mobile", "receiver_mobile")
    .withColumnRenamed("amount_clean", "amount")
    .withColumnRenamed("timestamp_clean", "transaction_timestamp")
    .withColumnRenamed("sender_mobile_masked", "sender_mobile")
    .withColumnRenamed("receiver_mobile_masked", "receiver_mobile")
)

# COMMAND ----------

# MAGIC %md ### Write Silver (merge on transaction_id) and the rejects quarantine table

# COMMAND ----------

silver_final_df.write.format("delta").mode("overwrite").option("mergeSchema", "true").saveAsTable(silver_table) \
    if not spark.catalog.tableExists(silver_table) else None

if spark.catalog.tableExists(silver_table):
    from delta.tables import DeltaTable
    silver_tbl = DeltaTable.forName(spark, silver_table)
    (
        silver_tbl.alias("tgt")
        .merge(silver_final_df.alias("src"), "tgt.transaction_id = src.transaction_id")
        .whenMatchedUpdateAll()
        .whenNotMatchedInsertAll()
        .execute()
    )
else:
    silver_final_df.write.format("delta").saveAsTable(silver_table)

invalid_df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(rejects_table)

# COMMAND ----------

# MAGIC %md ### Sanity check

# COMMAND ----------

silver_count = spark.table(silver_table).count()
reject_count = spark.table(rejects_table).count()
print(f"Silver table {silver_table}: {silver_count} valid rows.")
print(f"Rejects table {rejects_table}: {reject_count} rejected rows (cumulative).")
display(spark.table(silver_table).limit(10))

# COMMAND ----------

dbutils.notebook.exit(f"silver_table={silver_table};row_count={silver_count};rejects={reject_count}")
