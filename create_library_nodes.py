import geopandas as gpd
import pandas as pd

# Load SA2 boundaries
sa2 = gpd.read_file("data/raw/melbourne_sa2.json")
sa2 = sa2[sa2["GCC_NAME21"] == "Greater Melbourne"].copy()

# Load library counts
library_counts = pd.read_csv("data/processed/library_counts_by_sa2.csv")

# Fix join keys
sa2["SA2_CODE21"] = sa2["SA2_CODE21"].astype(str)
library_counts["SA2_CODE21"] = library_counts["SA2_CODE21"].astype(str)

# Join library count to SA2 geometry
nodes = sa2.merge(
    library_counts,
    on=["SA2_CODE21", "SA2_NAME21"],
    how="inner"
)

# Create centroid points from SA2 polygons
nodes["centroid"] = nodes.geometry.centroid
nodes["x"] = nodes["centroid"].x
nodes["y"] = nodes["centroid"].y

# Keep only fields needed for Vega-Lite
nodes_out = nodes[
    [
        "SA2_CODE21",
        "SA2_NAME21",
        "library_count",
        "x",
        "y"
    ]
]

nodes_out.to_csv(
    "data/processed/library_nodes.csv",
    index=False
)

print(nodes_out.head())
print("\nRows:", len(nodes_out))
print("\nDone!")