import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# 1) Read the CSV
# ------------------------------------------------
# Get project root (one level up from this script)
# ------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------
# Build path dynamically
# ------------------------------------------------
inputs_dir = PROJECT_ROOT / "inputs"
csv_path = inputs_dir / "exposure_2025.csv"

# ------------------------------------------------
# Read CSV
# ------------------------------------------------
df = pd.read_csv(csv_path)

print(f"Loaded file from: {csv_path}")# -----------------------------

#csv_path = "/Users/TrijotSinghIclooud/Downloads/medical-pricing-model/inputs/exposure_2025.csv"  # <-- change
#df = pd.read_csv(csv_path)

# Expected columns (rename if needed):
# - productID
# - premium_csv  (the premium coming from your CSV / policy admin)
# Plus any fields your model needs (age, region, plan, etc.)

# Safety: ensure premium is numeric
df["premium_csv"] = pd.to_numeric(df["premium"], errors="coerce")

# -----------------------------
# 2) Calculate premium from your other model
# -----------------------------
def calc_model_premium(row: pd.Series) -> float:
    """
    Replace this with your rating engine logic.
    Examples:
      - base_rate * product_factor * region_factor * age_factor
      - GLM/GBM prediction * exposure
      - Excel rating replicated in Python
    """
    # ---- SAMPLE DUMMY LOGIC (REPLACE) ----
    base_rate = 100.0

    # example factors (replace with your own mapping)
    product_factor = {
        "Basic": 1.00,
        "Premium": 1.15,
    }.get(str(row["product"]), 1.00)

    # optional: if column exists
    region_factor = 1.00
    if "region" in row.index:
        region_factor = {"DXB": 1.10, "AUH": 1.05}.get(str(row["region"]), 1.00)

    # optional: if column exists
    age_factor = 1.00
    if "age" in row.index and pd.notna(row["age"]):
        age = float(row["age"])
        age_factor = 1.0 + max(age - 30, 0) * 0.01  # toy example

    return base_rate * product_factor * region_factor * age_factor


# Apply rating model
df["premium_model"] = df.apply(calc_model_premium, axis=1)


# -----------------------------
# 3) Compare CSV premium vs model premium
# -----------------------------
# IMPORTANT: premiums rarely match exactly due to rounding / cents.
# Use a tolerance or rounding rule.
tolerance = 0.01  # $0.01 tolerance; change if needed

df["premium_diff"] = df["premium_model"] - df["premium_csv"]
df["match_flag"] = df["premium_diff"].abs() <= tolerance

# Optional: create match buckets for diagnostics (not required, but useful)
# e.g., "match", "0-1%", "1-5%", ">5%"
df["pct_diff"] = np.where(
    df["premium_csv"].abs() > 0,
    df["premium_diff"] / df["premium_csv"],
    np.nan
)

def bucket_pct(p):
    if pd.isna(p):
        return "missing_csv_premium"
    ap = abs(p)
    if ap <= 0.0001:   # ~0%
        return "match"
    if ap <= 0.05:     # 1%
        return "0-5%"
    if ap <= 0.10:     # 5%
        return "5%-50%"
    return ">10%"

df["match_bucket"] = df["pct_diff"].apply(bucket_pct)


# -----------------------------
# 4) Aggregate number of policies where premium matches by productID
# -----------------------------
# Count of policies + count matching + match rate
summary = (
    df.groupby("product")
      .agg(
          policies=("product", "size"),
          matched=("match_flag", "sum")
      )
      .reset_index()
)

summary["match_rate"] = summary["matched"] / summary["policies"]

# Sort for nicer charts
summary = summary.sort_values(["matched", "policies"], ascending=False)

print(summary.head(20))
