import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries containing river coordinates (WKT) and water levels
river_data = [
    {"name": "Lepsy River", "coordinates": "POINT (69.45783 50.21708)", "water_level": 10},
    {"name": "Shynzhaly River", "coordinates": "POINT (69.60000 50.08333)", "water_level": 12}
]

# Add rivers to the map with markers indicating water levels
for river in river_data:
    coords = wkt.loads(river["coordinates"]).coords[0]
    folium.Marker(location=[coords[1], coords[0]], popup=f"{river['name']} - Water Level: {river['water_level']} m").add_to(m)

# Save the final map
m.save("159.html")