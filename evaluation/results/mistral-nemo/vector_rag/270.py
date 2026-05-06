import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are Coordinates (WKT), create a hardcoded list of dictionaries
water_level_data = [
    {'date': '2021-01-01', 'level_cm': 50},
    {'date': '2021-02-01', 'level_cm': 60},
    # Add more data points as needed
]

# Function to calculate NDVI using water level data (for demonstration purposes)
def calculate_ndvi(water_level_data):
    ndvi_values = []
    for data_point in water_level_data:
        # For demonstration, we'll use a simple linear relationship between water level and NDVI
        ndvi = (data_point['level_cm'] / 100) * 2 - 1
        ndvi_values.append(ndvi)
    return ndvi_values

# Calculate NDVI using the water level data
ndvi_values = calculate_ndvi(water_level_data)

# Save the final map
m.save("270.html")