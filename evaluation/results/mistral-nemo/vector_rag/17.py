import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Create a hardcoded list of dictionaries for observations
observations = [
    {"type": "Observation", "name": "с.Tekes"},
    {"type": "Observation", "name": "с.Tekes"},
    {"type": "Observation", "name": "с.Tekes"},
    {"type": "Observation", "name": "с.Tekes"}
]

# Save the final map
m.save("17.html")