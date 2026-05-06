import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize folium map using the centroid of the shapefile
m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries for water level data (if available in the context)
water_level_data = [
    # Add dictionary entries here with keys: 'coordinates' (WKT), 'date', 'water_level', etc.
]

# Add water level data points to the map (if available)
for point in water_level_data:
    coordinates = wkt.loads(point['coordinates'])
    folium.CircleMarker(location=[coordinates.y, coordinates.x], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)

# Save the final map
m.save("252.html")