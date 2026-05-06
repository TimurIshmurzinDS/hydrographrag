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
    {"name": "Lepsy River (Lepsy aul)", "wkt": "POINT(78.5644 46.1406)"},
    {"name": "Lepsy River (Tolebaev aul)", "wkt": "POINT(78.1928 46.1725)"},
    {"name": "Turgen River (Tauturgen village)", "wkt": "POINT(77.3706 43.2057)"}
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("198.html")