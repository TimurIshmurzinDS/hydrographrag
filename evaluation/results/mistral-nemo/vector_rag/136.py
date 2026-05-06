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

# If context contains Coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': [longitude, latitude], 'properties': {'Water_level_Value': value, 'Date_water_level_Value': date, 'Water_level_Valuecm': water_level_cm, 'Water_quality_class': quality_class}},
    # Add more coordinates as needed
]

# Save the final map
m.save("136.html")