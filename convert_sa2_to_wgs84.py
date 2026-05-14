import geopandas as gpd

sa2 = gpd.read_file("data/raw/melbourne_sa2.json")

print("Original CRS:", sa2.crs)

# If CRS exists, convert to WGS84. If already WGS84, this keeps it compatible.
if sa2.crs is not None:
    sa2 = sa2.to_crs(epsg=4326)

sa2.to_file(
    "data/processed/melbourne_sa2_wgs84.json",
    driver="GeoJSON"
)

print("Created data/processed/melbourne_sa2_wgs84.json")
print("Done!")