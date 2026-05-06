import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads('POINT(51.5074 -0.1278)'), "properties": {"name": "Observation_2265"}},
    {"type": "Feature", "geometry": wkt.loads('POINT(51.5093 -0.1300)'), "properties": {"name": "Observation_2247"}},
    {"type": "Feature", "geometry": wkt.loads('POINT(51.5062 -0.1289)'), "properties": {"name": "Observation_2256"}},
    {"type": "Feature", "geometry": wkt.loads('POINT(51.5047 -0.1312)'), "properties": {"name": "Observation_2203"}}
]

# Add observations to the map
for obs in coordinates:
    folium.Marker(location=obs['geometry']['coordinates']).add_to(m)

# Save the final map
m.save("276.html")