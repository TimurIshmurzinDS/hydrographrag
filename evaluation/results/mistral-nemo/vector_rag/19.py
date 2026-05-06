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

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observations = [
    {'type': 'Обсервация', 'location': wkt.loads('POINT(12.3456 78.9012)')},
    {'type': 'Обсервация', 'location': wkt.loads('POINT(12.3456 78.9012)')},
    {'type': 'Обсервация', 'location': wkt.loads('POINT(12.3456 78.9012)')},
    {'type': 'Обсервация', 'location': wkt.loads('POINT(12.3456 78.9012)')}
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=[obs['location'].y, obs['location'].x], popup=obs['type']).add_to(m)

# Save the final map
m.save("19.html")