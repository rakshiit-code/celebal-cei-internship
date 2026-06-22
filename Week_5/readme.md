# Spark Data Processing Pipeline - Week 5 Assignment

This project demonstrates core Apache Spark fundamentals, including data cleaning, transformation, and aggregation using PySpark.

## Overview
This pipeline addresses common big data challenges by utilizing Spark's in-memory processing capabilities. The workflow focuses on:
- Handling missing data and duplicates.
- Transforming schema types for consistency.
- Performing wide transformations like `groupBy` for aggregation.

## Pipeline Steps
1. **Ingestion**: Reading raw CSV data into a Spark DataFrame.
2. [cite_start]**Cleaning**: Removing duplicate records and filling missing prices with `0`[cite: 15, 18, 19].
3. [cite_start]**Transformation**: Casting data types to ensure mathematical accuracy[cite: 11].
4. [cite_start]**Aggregation**: Calculating total revenue per `store_id`[cite: 20].

## Why Spark?
[cite_start]Traditional MapReduce processes data via disk-based storage, which introduces high latency[cite: 2]. [cite_start]Spark improves upon this by using **In-Memory Computing**, allowing for significantly faster iterative processing[cite: 3]. [cite_start]During grouping operations, Spark performs a "Shuffle"—a wide transformation where data is redistributed across the cluster to ensure consistency[cite: 12].

## Prerequisites
- Apache Spark (PySpark)
- Python 3.x

## How to Run
```bash
spark-submit your_script_name.py
