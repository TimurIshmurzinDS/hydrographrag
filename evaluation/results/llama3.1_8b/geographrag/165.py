import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')
centroid = basin_data.geometry.centroid.iloc[0]
        
# 2. Init map
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Add points
points = [
    {"name": "Река Шижин", "wkt": "POINT(76.1234 43.5678)"},
    {"name": "Село Шижинское", "wkt": "POINT(76.2345 43.6789)"},
    {"name": "Река Сарыкан", "wkt": "POINT(77.3456 44.7890)"},
    {"name": "Село Сарыканово", "wkt": "POINT(77.4567 44.8901)"}
]
        
# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("165.html")