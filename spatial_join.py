import pandas as pd
import geopandas as gpd

# =========================
# Load SA2 boundary polygons
# =========================
sa2 = gpd.read_file("data/raw/melbourne_sa2.json")

# Keep only Greater Melbourne
sa2 = sa2[sa2["GCC_NAME21"] == "Greater Melbourne"].copy()

# Clean SA2 name
sa2["SA2_NAME_clean"] = sa2["SA2_NAME21"].str.strip().str.lower()

# =========================
# Load library data
# =========================
libraries = pd.read_csv("data/raw/libraries.csv")

# Clean suburb name
libraries["Suburb_clean"] = libraries["Suburb"].str.strip().str.lower()

# =========================
# Manual suburb-to-SA2 mapping
# =========================
manual_mapping = {
    "melbourne": "Melbourne CBD - East",
    "docklands": "Docklands",
    "carlton": "Carlton",
    "east melbourne": "East Melbourne",
    "southbank": "Southbank - East",
    "st kilda": "St Kilda",
    "port melbourne": "Port Melbourne",
    "south melbourne": "South Melbourne",
    "albert park": "Albert Park",
    "richmond": "Richmond",
    "north fitzroy": "Fitzroy North",
    "brunswick": "Brunswick - South",
    "coburg": "Coburg - East",
    "preston": "Preston - West",
    "northcote": "Northcote - East",
    "reservoir": "Reservoir - East",
    "footscray": "Footscray",
    "sunshine": "Sunshine",
    "altona": "Altona",
    "newport": "Newport",
    "williamstown": "Williamstown",
    "box hill": "Box Hill",
    "doncaster": "Doncaster",
    "nunawading": "Nunawading",
    "camberwell": "Camberwell",
    "hawthorn": "Hawthorn",
    "kew": "Kew",
    "malvern": "Malvern - Glen Iris",
    "prahran": "Prahran - Windsor",
    "south yarra": "South Yarra - West",
    "oakleigh": "Oakleigh - Huntingdale",
    "clayton": "Clayton",
    "glen waverley": "Glen Waverley - East",
    "mount waverley": "Mount Waverley - North",
    "wheelers hill": "Wheelers Hill",
    "dandenong": "Dandenong",
    "springvale": "Springvale",
    "noble park": "Noble Park",
    "narre warren": "Narre Warren - North",
    "cranbourne": "Cranbourne",
    "hampton park": "Hampton Park - Lynbrook",
    "frankston": "Frankston",
    "mornington": "Mornington",
    "cheltenham": "Cheltenham",
    "sandringham": "Sandringham",
    "brighton": "Brighton",
    "eltham": "Eltham",
    "greensborough": "Greensborough",
    "rosanna": "Heidelberg - Rosanna",
    "werribee": "Werribee - South",
    "point cook": "Point Cook - South",
    "tarneit": "Tarneit",
    "melton": "Melton",
    "sunbury": "Sunbury",
    "craigieburn": "Craigieburn - Mickleham",
    "broadmeadows": "Broadmeadows",
    "cobblebank": "Melton South",
    "geelong": "Geelong"
}

# Apply manual mapping
libraries["Mapped_SA2"] = libraries["Suburb_clean"].map(manual_mapping)
libraries["Mapped_SA2_clean"] = libraries["Mapped_SA2"].str.strip().str.lower()

# =========================
# Join libraries to SA2
# =========================
matched = libraries.merge(
    sa2[["SA2_CODE21", "SA2_NAME21", "SA2_NAME_clean"]],
    left_on="Mapped_SA2_clean",
    right_on="SA2_NAME_clean",
    how="left"
)

# Save unmatched rows for checking
unmatched = matched[matched["SA2_CODE21"].isna()]
unmatched.to_csv("data/processed/unmatched_libraries.csv", index=False)

# Count libraries per SA2
library_counts = (
    matched.dropna(subset=["SA2_CODE21"])
    .groupby(["SA2_CODE21", "SA2_NAME21"])
    .size()
    .reset_index(name="library_count")
)

# Save library counts
library_counts.to_csv(
    "data/processed/library_counts_by_sa2.csv",
    index=False
)

# =========================
# Print check results
# =========================
print("Total libraries:", len(libraries))
print("Matched libraries:", matched["SA2_CODE21"].notna().sum())
print("Unmatched libraries:", matched["SA2_CODE21"].isna().sum())

print("\nUnmatched rows:")
print(unmatched[["Library", "Suburb", "Mapped_SA2"]])

print("\nLibrary counts preview:")
print(library_counts.head())

print("\nDone!")