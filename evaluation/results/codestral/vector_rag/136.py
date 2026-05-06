import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for water level sensors (replace with actual data)
sensors = [
    {"id": 1, "location": wkt.loads("POINT (-74.0060 40.7128)"), "water_level": 50, "quality_class": "A"},
    # Add more sensors as needed
]

# Add water level sensors to the map
for sensor in sensors:
    folium.CircleMarker(location=[sensor["location"].y, sensor["location"].x], radius=6, color='blue', fill=True, fill_color='blue').add_to(m)

# Save the final map
m.save("136.html")