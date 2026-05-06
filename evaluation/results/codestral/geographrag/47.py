import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin (Assuming a placeholder for basin data)
basin_data = None
centroid = [43.3333618, 78.4793574] # Using the centroid of above Bartogay Reservoir as a placeholder

# 2. Init map
m = folium.Map(location=centroid, tiles='CartoDB positron', zoom_start=8)

# 3. Add points based on Graph Knowledge
points = [
    {"name": "above Bartogay Reservoir", "wkt": "POINT(78.4793574 43.3333618)"},
    {"name": "Malybay village", "wkt": "POINT(78.2424 43.2928)"}
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("47.html")