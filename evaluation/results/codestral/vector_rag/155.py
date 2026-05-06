import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize the map
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for rivers and village coordinates (WKT format)
data = [
    {"name": "Bayankol River", "coordinates": "POINT (73.123456 53.123456)"},
    {"name": "Lepsy River", "coordinates": "POINT (73.678901 53.678901)"},
    {"name": "Bayankol village", "coordinates": "POINT (73.234567 53.234567)"}
]

# Add rivers and village to the map
for item in data:
    point = wkt.loads(item["coordinates"])
    folium.Marker([point.y, point.x], popup=item["name"]).add_to(m)

# Save the final map
m.save("155.html")