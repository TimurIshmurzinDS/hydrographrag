import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid.iloc[0]
        
# 2. Init map
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Add YOUR points here based on Graph Knowledge
points = [
    {"name": "Добын пир", "wkt": "POINT(80.046 43.4)"},
    {"name": "164 км выше ГЭС Капчагай", "wkt": "POINT(79.590664 43.977649)"},
    {"name": "Капчагайский тракт", "wkt": "POINT(77.29 43.49)"},
    {"name": "1 км ниже ветвления Жидели", "wkt": "POINT(79.988607 44.00253)"},
    {"name": "Акзхараул", "wkt": "POINT(80.3849 45.4753)"}
]
        
# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("164.html")