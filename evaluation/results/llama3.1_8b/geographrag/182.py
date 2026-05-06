import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin (пропустим, так как данные отсутствуют)
basin_data = None

# 2. Init map
m = folium.Map(location=[52.0, 61.0], tiles='CartoDB positron', zoom_start=8)

# 3. Add points based on Graph Knowledge
points = [
    {"name": "Река Уржар", "wkt": "POINT(61.0 52.0)"},
    # Другие точки можно добавить аналогично
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("182.html")