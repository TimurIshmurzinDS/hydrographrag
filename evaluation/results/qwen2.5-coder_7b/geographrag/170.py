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
    {"name": "Ручье Терисбутак", "wkt": "POINT(76.0 43.0)"},
    {"name": "Основная артерия 1", "wkt": "LINESTRING(75.5 42.8, 76.5 43.2)"},
    {"name": "Основная артерия 2", "wkt": "LINESTRING(76.0 43.2, 77.0 43.5)"},
    {"name": "Вторичная ветвь 1", "wkt": "LINESTRING(76.2 43.1, 76.8 43.3)"},
    {"name": "Вторичная ветвь 2", "wkt": "LINESTRING(76.5 43.3, 77.0 43.4)"}
]
        
# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("170.html")