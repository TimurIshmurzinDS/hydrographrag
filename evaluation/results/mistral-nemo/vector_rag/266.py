import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# If there are coordinates in WKT format in the context, create a hardcoded list of dictionaries
fields = [
    {'name': 'Field 1', 'geometry': wkt.loads('POINT(49.83576 -36.24044)')},
    {'name': 'Field 2', 'geometry': wkt.loads('POINT(49.84234 -36.23891)')}
]

# Add fields to the map
for field in fields:
    folium.Marker(field['geometry'], popup=field['name']).add_to(m)

# Save the final map
m.save("266.html")