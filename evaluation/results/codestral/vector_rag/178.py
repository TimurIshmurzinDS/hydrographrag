import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.geometry.centroid.y, basin.geometry.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for rivers (replace with actual coordinates if available)
rivers = [
    {"name": "Tentek River", "coordinates": "LINESTRING(...)" },
    {"name": "Tekes River", "coordinates": "LINESTRING(...)" },
    {"name": "Temirlik River", "coordinates": "LINESTRING(...)" },
    {"name": "Tekeli River", "coordinates": "LINESTRING(...)" }
]

# Add rivers to the map
for river in rivers:
    folium.GeoJson(wkt.loads(river["coordinates"]), style_function=lambda x: {'color': 'blue'}).add_child(folium.Popup(river["name"])).add_to(m)

# Save the final map
m.save("178.html")