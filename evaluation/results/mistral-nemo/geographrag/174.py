import geopandas as gpd
import folium
from shapely import wkt

# 1. Load basin data for Emel river only (as Tenteck's data is missing)
emel_data = gpd.read_file(r"data/emel_basin.shp").to_crs('EPSG:4326')
centroid = emel_data.geometry.centroid.iloc[0]

# 2. Init map
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)
folium.GeoJson(emel_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# 3. Add Emel river points here based on Graph Knowledge
points = [
    {"name": "Emel River", "wkt": "POINT(76.0 43.0)"}
]

# 4. Draw markers
for p in points:
    geom = wkt.loads(p["wkt"])
    folium.Marker(location=[geom.y, geom.x], popup=p["name"]).add_to(m)

m.save("174.html")