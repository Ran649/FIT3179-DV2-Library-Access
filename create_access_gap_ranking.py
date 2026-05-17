import pandas as pd
import geopandas as gpd

# Load Greater Melbourne SA2 boundary
sa2 = gpd.read_file("data/processed/melbourne_sa2_wgs84.json")
sa2["SA2_CODE21"] = sa2["SA2_CODE21"].astype(str)

melbourne_codes = sa2["SA2_CODE21"].unique()

# Load master table
master = pd.read_csv("data/processed/master_sa2.csv")
master["SA2_CODE21"] = master["SA2_CODE21"].astype(str)

# Keep only Greater Melbourne SA2s
melbourne = master[master["SA2_CODE21"].isin(melbourne_codes)].copy()

# Fill missing values
melbourne["library_count"] = melbourne["library_count"].fillna(0)
melbourne["libraries_per_10000"] = melbourne["libraries_per_10000"].fillna(0)

# Create preliminary access gap score
# Higher population + lower library access = worse access gap
melbourne["access_gap_score"] = (
    melbourne["population"] * (1 / (melbourne["libraries_per_10000"] + 0.1))
)

# Keep only SA2s with no or very low access
low_access = melbourne[melbourne["libraries_per_10000"] <= 0.1].copy()

# Rank worst 15
worst15 = low_access.sort_values(
    by="access_gap_score",
    ascending=False
).head(15)

worst15 = worst15[
    [
        "SA2_CODE21",
        "SA2_NAME21",
        "population",
        "library_count",
        "libraries_per_10000",
        "IRSD_score",
        "IRSD_decile",
        "access_gap_score"
    ]
]

worst15.to_csv("data/processed/access_gap_worst15.csv", index=False)

print(worst15)
print("\nCreated data/processed/access_gap_worst15.csv")