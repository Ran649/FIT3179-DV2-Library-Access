import geopandas as gpd
import pandas as pd

nodes = pd.read_csv("data/processed/library_nodes.csv")

gdf = gpd.GeoDataFrame(
    nodes,
    geometry=gpd.points_from_xy(nodes["x"], nodes["y"]),
    crs="EPSG:4326"
)

gdf = gdf.to_crs(epsg=3111)
gdf["geometry"] = gdf.geometry.buffer(1000)
gdf = gdf.to_crs(epsg=4326)

gdf.to_file(
    "data/processed/library_buffers.geojson",
    driver="GeoJSON"
)

print("Created data/processed/library_buffers.geojson")