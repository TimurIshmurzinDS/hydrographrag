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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'Point', 'coordinates': [41.7325, 68.9167]},  # Example coordinate for Temirlik village
]

# Create a GeoDataFrame from the coordinates
points = gpd.GeoDataFrame(coordinates, geometry=[wkt.loads(c['type']) for c in coordinates])

# Add points to the map
for _, point in points.iterrows():
    folium.Marker([point.geometry.y, point.geometry.x]).add_to(m)

# Save the final map
m.save("115.html")