import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize the map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=10)

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for Coordinates (WKT) if available in context
coordinates = [
    {'name': 'Point 1', 'geometry': wkt.loads('POINT (-76.985643 42.688089)')},
    {'name': 'Point 2', 'geometry': wkt.loads('POINT (-76.985643 42.688089)')},
]

# Add points to the map (if available)
for point in coordinates:
    folium.Marker(location=[point['geometry'].y, point['geometry'].x], popup=point['name']).add_to(m)

# Save the map
m.save("266.html")