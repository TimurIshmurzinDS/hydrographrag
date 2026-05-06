import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin (Assuming a placeholder for this step)
basin_data = None
centroid = [78, 45] # Using approximate coordinates of Jetisu Region

# 2. Init map
m = folium.Map(location=centroid, tiles='CartoDB positron', zoom_start=8)

# 3. Add points based on Graph Knowledge
points = [
    {"name": "Aynabulak railway station", "wkt": "POINT(77.994303 44.623949)"}
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("50.html")