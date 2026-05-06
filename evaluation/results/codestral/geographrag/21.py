import geopandas as gpd
import folium
from shapely import wkt

# 1. Init map (Since basin data is not available, we'll use the coordinates of Tekeli town)
m = folium.Map(location=[44.5147, 69.8757], tiles='CartoDB positron', zoom_start=8)

# 2. Add points based on Graph Knowledge
points = [
    {"name": "Tekeli town", "wkt": "POINT(69.8757 44.5147)"}
]

# 3. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("21.html")