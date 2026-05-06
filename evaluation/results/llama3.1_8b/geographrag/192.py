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
    {"name": "Река Бутак", "wkt": "POINT(76.5 43.1)"},
    {"name": "Сельскохозяйственные угодья", "wkt": "POLYGON ((75.9 42.8, 76.2 42.8, 76.2 43.3, 75.9 43.3, 75.9 42.8))"},
    {"name": "Лесной массив", "wkt": "POLYGON ((77.1 43.5, 77.4 43.5, 77.4 44.0, 77.1 44.0, 77.1 43.5))"}
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("192.html")