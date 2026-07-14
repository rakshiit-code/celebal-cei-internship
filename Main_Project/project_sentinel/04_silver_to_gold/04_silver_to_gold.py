# Databricks notebook source
# MAGIC %md
# MAGIC # Project Sentinel — Step 4: Silver to Gold
# MAGIC
# MAGIC Aggregates cleansed Silver data into business-facing Gold tables:
# MAGIC 1. `gold_daily_kpis` — total volume, transaction counts, success rate, avg ticket size.
# MAGIC 2. `gold_fraud_flags` — a simple, explainable rule-based fraud score per transaction.
# MAGIC 3. `gold_fraud_summary` — daily rollup of flagged activity for a dashboard.
# MAGIC
# MAGIC The fraud scoring here is intentionally simple/rule-based (per the doc's "simple
# MAGIC fraud scoring" requirement) rather than a trained model — easy to explain, easy to
# MAGIC extend later.

# COMMAND ----------

dbutils.widgets.text("catalog", "sentinel_catalog", "Unity Catalog Catalog")
dbutils.widgets.text("schema", "sentinel", "Schema")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

silver_table = f"{catalog}.{schema}.silver_upi_transactions"
gold_kpi_table = f"{catalog}.{schema}.gold_daily_kpis"
gold_fraud_table = f"{catalog}.{schema}.gold_fraud_flags"
gold_fraud_summary_table = f"{catalog}.{schema}.gold_fraud_summary"

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.window import Window

silver_df = spark.table(silver_table).withColumn("txn_date", F.to_date("transaction_timestamp"))

# COMMAND ----------

# MAGIC %md ## 4a. Business KPIs

# COMMAND ----------

kpi_df = (
    silver_df
    .groupBy("txn_date")
    .agg(
        F.count("*").alias("total_transactions"),
        F.sum("amount").alias("total_volume"),
        F.avg("amount").alias("avg_ticket_size"),
        F.sum(F.when(F.col("status") == "SUCCESS", 1).otherwise(0)).alias("successful_transactions"),
        F.sum(F.when(F.col("status") == "FAILED", 1).otherwise(0)).alias("failed_transactions"),
        F.sum(F.when(F.col("status") == "PENDING", 1).otherwise(0)).alias("pending_transactions"),
        F.countDistinct("sender_vpa").alias("unique_senders"),
        F.countDistinct("receiver_vpa").alias("unique_receivers"),
    )
    .withColumn(
        "success_rate_pct",
        F.round(F.col("successful_transactions") / F.col("total_transactions") * 100, 2)
    )
    .withColumn("_gold_load_timestamp", F.current_timestamp())
)

kpi_df.write.format("delta").mode("overwrite").option("mergeSchema", "true").saveAsTable(gold_kpi_table)

# COMMAND ----------

# MAGIC %md ## 4b. Fraud scoring (rule-based)
# MAGIC
# MAGIC Each transaction gets points added for known fraud signals; the sum is the score:
# MAGIC
# MAGIC | Signal | Points | Rationale |
# MAGIC |---|---|---|
# MAGIC | Amount > 95th percentile of the day | 30 | Unusually large transfer |
# MAGIC | Same sender makes 5+ transactions within a 10-minute window | 30 | Rapid-fire burst pattern |
# MAGIC | Sender total volume in last 10 min > ₹1,00,000 | 25 | Sudden high-value spike |
# MAGIC | Transaction failed/pending but amount is very high | 15 | High-value transaction not confirmed |
# MAGIC
# MAGIC Score >= 50 → `HIGH`, 25-49 → `MEDIUM`, else `LOW`.

# COMMAND ----------

# 95th percentile amount per day, for the "unusually large" signal
p95_df = (
    silver_df.groupBy("txn_date")
    .agg(F.expr("percentile_approx(amount, 0.95)").alias("p95_amount"))
)

scored_df = silver_df.join(p95_df, on="txn_date", how="left")

# Rolling 10-minute sender activity window, using a time-based window join on Spark SQL
sender_window = (
    Window.partitionBy("sender_vpa")
    .orderBy(F.col("transaction_timestamp").cast("long"))
    .rangeBetween(-600, 0)  # 600 seconds = 10 minutes
)

scored_df = (
    scored_df
    .withColumn("sender_txn_count_10min", F.count("transaction_id").over(sender_window))
    .withColumn("sender_volume_10min", F.sum("amount").over(sender_window))
    .withColumn("signal_large_amount", (F.col("amount") > F.col("p95_amount")).cast("int") * 30)
    .withColumn("signal_burst_pattern", (F.col("sender_txn_count_10min") >= 5).cast("int") * 30)
    .withColumn("signal_volume_spike", (F.col("sender_volume_10min") > 100000).cast("int") * 25)
    .withColumn(
        "signal_unconfirmed_high_value",
        ((F.col("status") != "SUCCESS") & (F.col("amount") > 50000)).cast("int") * 15
    )
    .withColumn(
        "fraud_score",
        F.col("signal_large_amount") + F.col("signal_burst_pattern")
        + F.col("signal_volume_spike") + F.col("signal_unconfirmed_high_value")
    )
    .withColumn(
        "fraud_risk_level",
        F.when(F.col("fraud_score") >= 50, "HIGH")
         .when(F.col("fraud_score") >= 25, "MEDIUM")
         .otherwise("LOW")
    )
    .withColumn("_gold_load_timestamp", F.current_timestamp())
)

fraud_flags_df = scored_df.select(
    "transaction_id", "txn_date", "transaction_timestamp", "sender_vpa", "receiver_vpa",
    "amount", "status", "ip_address", "transaction_type",
    "signal_large_amount", "signal_burst_pattern", "signal_volume_spike",
    "signal_unconfirmed_high_value", "fraud_score", "fraud_risk_level",
    "_gold_load_timestamp"
)

fraud_flags_df.write.format("delta").mode("overwrite").option("mergeSchema", "true").saveAsTable(gold_fraud_table)

# COMMAND ----------

# MAGIC %md ## 4c. Daily fraud summary (for dashboarding)

# COMMAND ----------

fraud_summary_df = (
    fraud_flags_df.groupBy("txn_date")
    .agg(
        F.count("*").alias("total_transactions"),
        F.sum(F.when(F.col("fraud_risk_level") == "HIGH", 1).otherwise(0)).alias("high_risk_count"),
        F.sum(F.when(F.col("fraud_risk_level") == "MEDIUM", 1).otherwise(0)).alias("medium_risk_count"),
        F.sum(F.when(F.col("fraud_risk_level") == "LOW", 1).otherwise(0)).alias("low_risk_count"),
        F.sum(F.when(F.col("fraud_risk_level") == "HIGH", F.col("amount")).otherwise(0)).alias("high_risk_volume"),
    )
    .withColumn(
        "high_risk_rate_pct",
        F.round(F.col("high_risk_count") / F.col("total_transactions") * 100, 2)
    )
    .withColumn("_gold_load_timestamp", F.current_timestamp())
)

fraud_summary_df.write.format("delta").mode("overwrite").option("mergeSchema", "true").saveAsTable(gold_fraud_summary_table)

# COMMAND ----------

# MAGIC %md ### Sanity check

# COMMAND ----------

print(f"Gold KPI table: {gold_kpi_table}")
display(spark.table(gold_kpi_table))

print(f"Gold fraud flags table: {gold_fraud_table}")
display(spark.table(gold_fraud_table).orderBy(F.col("fraud_score").desc()).limit(10))

print(f"Gold fraud summary table: {gold_fraud_summary_table}")
display(spark.table(gold_fraud_summary_table))

# COMMAND ----------

dbutils.notebook.exit(f"gold_kpi_table={gold_kpi_table};gold_fraud_table={gold_fraud_table}")
