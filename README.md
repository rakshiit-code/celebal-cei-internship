# Celebal Technologies: Data Science Internship Portfolio

Repository tracking the 8-week enterprise analytics training modules and industrial data pipeline projects.

## Project Directory
* **Week 1:** Basic Data Exploration and Cleaning using Pandas

---

## Module 1: Enterprise E-Commerce Data Exploration & Cleansing
* **Core Toolkit:** Python, Pandas, NumPy, Glob, OS Virtual Layer
* **Dataset Target:** Multiclass Shopping Purchase Ledger (99 Consolidations)

### Key Engineering Implementation Matrix
1. **Automated Ingestion Pipeline:** Programmatically targeted and consolidated 99 individual split file parts from the raw storage layer into a unified dataframe footprint.
2. **Data Sanitization Operations:**
   * **Redundancy Sweep:** Dropped transaction-level duplicates to maintain absolute analytical variance.
   * **Missing Value Imputation:** Fixed missing attributes using numeric column-specific medians and categorical modes to preserve database completeness without inducing data skew.
3. **Feature Derivation:** Implemented safe type-conversion and executed vectorized matrix multiplication to construct a clean, operational `total_amount` metric ($Total = Unit Price \times Quantity$).
4. **Deliverable Pipeline:** Generated fully documented interactive Jupyter logic notebook alongside the final verified dataset artifact `cleaned_shopping_dataset.csv`.
