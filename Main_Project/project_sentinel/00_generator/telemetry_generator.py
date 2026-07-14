# Databricks notebook source
# MAGIC %md
# MAGIC # Project Sentinel — Step 0: Telemetry Generator
# MAGIC
# MAGIC Simulates high-throughput JSON UPI transaction payloads and drops them into a
# MAGIC Unity Catalog **Volume** as the raw source. Two kinds of "bad data" are injected
# MAGIC on purpose so downstream layers have real work to do:
# MAGIC
# MAGIC 1. **Structural corruption** — nulls, whitespace-padded numbers, negative amounts,
# MAGIC    type mismatches (amount sent as a string), missing fields.
# MAGIC 2. **Logical fraud anomalies** — bursts of unusually large transactions from a small
# MAGIC    pool of "suspicious" IPs / senders in a tight time window.
# MAGIC
# MAGIC No dataset is shipped with this project — everything below is generated at run time.

# COMMAND ----------

# MAGIC %md ### Widgets (parameters)

# COMMAND ----------

dbutils.widgets.text("catalog", "sentinel_catalog", "Unity Catalog Catalog")
dbutils.widgets.text("schema", "sentinel", "Schema")
dbutils.widgets.text("volume", "raw_telemetry", "Volume name")
dbutils.widgets.text("num_files", "10", "Number of JSON files to generate")
dbutils.widgets.text("records_per_file", "500", "Records per file")
dbutils.widgets.text("fraud_ratio", "0.03", "Fraction of records that are fraud-flagged spikes")
dbutils.widgets.text("corruption_ratio", "0.15", "Fraction of records with structural corruption")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
volume = dbutils.widgets.get("volume")
num_files = int(dbutils.widgets.get("num_files"))
records_per_file = int(dbutils.widgets.get("records_per_file"))
fraud_ratio = float(dbutils.widgets.get("fraud_ratio"))
corruption_ratio = float(dbutils.widgets.get("corruption_ratio"))

volume_path = f"/Volumes/{catalog}/{schema}/{volume}"

# COMMAND ----------

# MAGIC %md ### Setup: catalog / schema / volume

# COMMAND ----------

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.{volume}")
dbutils.fs.mkdirs(volume_path)

# COMMAND ----------

# MAGIC %md ### Generator logic

# COMMAND ----------

import json
import random
import string
import uuid
from datetime import datetime, timedelta, timezone

random.seed()  # non-deterministic, real-world-ish

BANKS = ["okhdfcbank", "okicici", "oksbi", "okaxis", "ybl", "paytm", "apl"]
FIRST_NAMES = ["rahul", "priya", "amit", "sneha", "vikram", "anita", "arjun",
               "kavya", "rohan", "neha", "suresh", "pooja", "manish", "divya"]
TXN_TYPES = ["P2P", "P2M", "BILL_PAY", "RECHARGE"]
STATUSES = ["SUCCESS", "FAILED", "PENDING"]
STATUS_WEIGHTS = [0.85, 0.10, 0.05]

# A small fixed pool of "suspicious" IPs / devices used to simulate coordinated fraud bursts
SUSPICIOUS_IPS = ["185.220.101.7", "45.155.204.19", "194.26.29.14", "89.248.165.32"]
SUSPICIOUS_SENDERS = [f"fraudster{i}@{random.choice(BANKS)}" for i in range(5)]

def random_ip(suspicious=False):
    if suspicious:
        return random.choice(SUSPICIOUS_IPS)
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def random_vpa():
    return f"{random.choice(FIRST_NAMES)}{random.randint(1,999)}@{random.choice(BANKS)}"

def random_mobile():
    return f"9{random.randint(100000000, 999999999)}"

def random_timestamp(base_time, jitter_minutes=1440):
    return base_time - timedelta(minutes=random.randint(0, jitter_minutes),
                                  seconds=random.randint(0, 59))

def base_record(base_time, fraud=False):
    ts = random_timestamp(base_time, jitter_minutes=5 if fraud else 1440)
    sender = random.choice(SUSPICIOUS_SENDERS) if fraud else random_vpa()
    amount = round(random.uniform(50000, 200000), 2) if fraud else round(random.uniform(10, 25000), 2)
    return {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S"),
        "sender_vpa": sender,
        "receiver_vpa": random_vpa(),
        "amount": amount,
        "currency": "INR",
        "status": random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0],
        "device_id": f"dev-{uuid.uuid4().hex[:10]}",
        "ip_address": random_ip(suspicious=fraud),
        "transaction_type": random.choice(TXN_TYPES),
        "bank_ref_no": f"BR{random.randint(10**9, 10**10 - 1)}",
        "sender_mobile": random_mobile(),
        "receiver_mobile": random_mobile(),
        "is_fraud_seed": fraud,  # ground-truth label kept only for later validation/demo purposes
    }

def corrupt_record(rec):
    """Randomly injects one or more structural corruptions into a record."""
    corruption_types = random.sample(
        ["null_amount", "whitespace_amount", "negative_amount", "string_amount",
         "null_timestamp", "malformed_timestamp", "missing_field", "null_vpa"],
        k=random.randint(1, 2)
    )
    for c in corruption_types:
        if c == "null_amount":
            rec["amount"] = None
        elif c == "whitespace_amount":
            rec["amount"] = f"  {rec['amount']}  "
        elif c == "negative_amount":
            rec["amount"] = -abs(float(rec["amount"])) if isinstance(rec["amount"], (int, float)) else rec["amount"]
        elif c == "string_amount":
            rec["amount"] = str(rec["amount"])
        elif c == "null_timestamp":
            rec["timestamp"] = None
        elif c == "malformed_timestamp":
            rec["timestamp"] = "31-13-2026 99:99"
        elif c == "missing_field":
            field = random.choice(["device_id", "bank_ref_no", "receiver_mobile"])
            rec.pop(field, None)
        elif c == "null_vpa":
            rec["sender_vpa"] = None
    return rec

def generate_file(n_records, fraud_ratio, corruption_ratio, base_time):
    records = []
    for _ in range(n_records):
        is_fraud = random.random() < fraud_ratio
        rec = base_record(base_time, fraud=is_fraud)
        if random.random() < corruption_ratio:
            rec = corrupt_record(rec)
        records.append(rec)
    random.shuffle(records)
    return records

# COMMAND ----------

# MAGIC %md ### Write generated files to the Volume

# COMMAND ----------

now = datetime.now(timezone.utc)
written_files = []

for i in range(num_files):
    batch_time = now - timedelta(minutes=i * 5)
    records = generate_file(records_per_file, fraud_ratio, corruption_ratio, batch_time)
    file_name = f"upi_telemetry_{batch_time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.json"
    local_path = f"/tmp/{file_name}"

    # Newline-delimited JSON — one payload per line, mirroring a streaming telemetry feed
    with open(local_path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    dest_path = f"{volume_path}/{file_name}"
    dbutils.fs.cp(f"file:{local_path}", dest_path)
    written_files.append(dest_path)

print(f"Generated {num_files} files ({records_per_file} records each) into {volume_path}")
for p in written_files:
    print(" -", p)

# COMMAND ----------

dbutils.notebook.exit(json.dumps({"volume_path": volume_path, "files_written": len(written_files)}))
