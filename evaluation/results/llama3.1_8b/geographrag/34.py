import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid.iloc[0]
        
# 2. Init map
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Add points based on Graph Knowledge
points = [
    {"name": "Река Лепси", "wkt": "POINT(27.5 59.5)"},
    {"name": "Сельскохозяйственные стоки", "wkt": "POINT(28.2 60.1)"},
    {"name": "Промышленный сброс", "wkt": "POINT(26.8 58.9)"}
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("34.html")