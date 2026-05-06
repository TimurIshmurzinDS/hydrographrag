import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(gdf.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT), create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': [longitude, latitude], 'properties': {'name': 'Point Name'}},
    # Add more points as needed
]

for coord in coordinates:
    folium.Marker(location=coord['coordinates']).add_to(m)

# Save the final map
m.save("277.html")