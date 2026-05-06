import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are Coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Shilik River', 'wkt': 'LINESTRING(-75.123 40.123, -75.234 40.234)'},
    # Add more coordinates as needed
]

# Save the final map
m.save("47.html")