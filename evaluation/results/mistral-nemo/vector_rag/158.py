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
    {'name': 'Bayankol River', 'wkt': 'LINESTRING(...)'},  # Replace (...) with actual WKT coordinates
    {'name': 'Sarykan River', 'wkt': 'LINESTRING(...)'}   # Replace (...) with actual WKT coordinates
]

# Add rivers to the map using folium.GeoJson
for river in coordinates:
    wkt_river = wkt.loads(river['wkt'])
    folium.GeoJson(wkt_river, fillColor='blue', color='black', fillOpacity=0.5).add_to(m)

# Save the final map
m.save("158.html")