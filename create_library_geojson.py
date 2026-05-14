import pandas as pd
import json

# Read library node data
df = pd.read_csv("data/processed/library_nodes.csv")

features = []

for _, row in df.iterrows():

    feature = {
        "type": "Feature",
        "properties": {
            "SA2_NAME21": row["SA2_NAME21"],
            "library_count": row["library_count"]
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(row["x"]),
                float(row["y"])
            ]
        }
    }

    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("data/processed/library_nodes.geojson", "w") as f:
    json.dump(geojson, f)

print("GeoJSON created!")