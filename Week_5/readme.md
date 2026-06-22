# Spark Data Processing Pipeline - Week 5 Assignment

This project demonstrates core Apache Spark fundamentals, including data cleaning, transformation, and aggregation using PySpark.

## Overview
This pipeline addresses common big data challenges by utilizing Spark's in-memory processing capabilities. The workflow focuses on:
- Handling missing data and duplicates.
- Transforming schema types for consistency.
- Performing wide transformations like `groupBy` for aggregation.

## Pipeline Steps
1. **Ingestion**: Reading raw CSV data into a Spark DataFrame.
2. **Cleaning**: Removing duplicate records and filling missing prices with `0.
3. **Transformation**: Casting data types to ensure mathematical accuracy.
4. **Aggregation**: Calculating total revenue per store_id.

## What's in the notebook

1. **Spark vs MapReduce** — limitations of MapReduce, advantages of Spark (in-memory computing, DAG execution).
2. **Spark session setup** and **data loading** (schema, row count, sample rows).
3. **Data cleaning** — duplicate removal, null handling (`drop` vs `fill`).
4. **Filtering** — by age range, category, region.
5. **Transformation** — renaming columns, casting types.
6. **Aggregation** — `count`, `sum`, `avg`, `min`, `max`.
7. **Grouping** — `groupBy` with conditions on aggregated results.
8. **Wide transformations & shuffle** — conceptual explanation.
9. **Schema modification** — casting `raw_timestamp` to `TimestampType`, renaming to `event_time`.
10. **Handling inconsistent data** — nulls, empty strings.
11. **Complete pipeline** — clean → filter → transform → aggregate, in one chain.
12. **Q&A section (Q1–Q15)** — every assignment question answered with explanation and/or runnable PySpark code and real captured output.
13. **Insights** — observations on data quality, null handling, and performance (shuffle cost).

## Why Spark?
Traditional MapReduce processes data via disk-based storage, which introduces high latency. Spark improves upon this by using **In-Memory Computing**, allowing for significantly faster iterative processing. During grouping operations, Spark performs a "Shuffle"—a wide transformation where data is redistributed across the cluster to ensure consistency.

## Prerequisites
- Apache Spark (PySpark)
- Python 3.x

## How to run

```bash
pip install pyspark
jupyter notebook notebook/spark_basics.ipynb
```

All cells run end-to-end with no errors using `pyspark` in local mode (`local[*]`).
