import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid.iloc[0]
        
# 2. Init map
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Add points here based on Graph Knowledge
points = [
    {"name": "Река Батареки River", "wkt": "POINT(76.0 43.0)"},
    {"name": "Максимальный уровень воды", "wkt": "POINT(75.5 42.8)"},
    {"name": "Минимальный уровень воды", "wkt": "POINT(76.2 43.1)"},
    {"name": "Средний уровень воды", "wkt": "POINT(75.9 42.9)"}
]
        
# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("14.html")