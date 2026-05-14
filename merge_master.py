import pandas as pd

# =========================
# Load datasets
# =========================

seifa = pd.read_csv("data/processed/seifa_clean.csv")
library_counts = pd.read_csv("data/processed/library_counts_by_sa2.csv")

# =========================
# Fix join key type
# =========================

seifa["SA2_CODE21"] = seifa["SA2_CODE21"].astype(str)
library_counts["SA2_CODE21"] = library_counts["SA2_CODE21"].astype(str)

seifa["SA2_NAME21"] = seifa["SA2_NAME21"].astype(str).str.strip()
library_counts["SA2_NAME21"] = library_counts["SA2_NAME21"].astype(str).str.strip()

# =========================
# Merge datasets
# =========================

master = seifa.merge(
    library_counts,
    on=["SA2_CODE21", "SA2_NAME21"],
    how="left"
)

# Fill missing library counts with 0
master["library_count"] = master["library_count"].fillna(0)

# =========================
# Create derived metrics
# =========================

master["libraries_per_10000"] = (
    master["library_count"] / master["population"]
) * 10000

# =========================
# Save master dataset
# =========================

master.to_csv(
    "data/processed/master_sa2.csv",
    index=False
)

# =========================
# Preview
# =========================

print(master.head())
print("\nRows:", len(master))
print("\nNumber of SA2s with libraries:", (master["library_count"] > 0).sum())
print("\nDone!")