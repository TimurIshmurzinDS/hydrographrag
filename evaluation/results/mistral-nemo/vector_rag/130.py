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
bayankol_river = {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('LINESTRING(...)'), 'properties': {'name': 'Bayankol River'}}]}
shilik_river = {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('LINESTRING(...)'), 'properties': {'name': 'Shilik River'}}]}

# Add rivers to the map
folium.GeoJson(bayankol_river, fillColor='blue', color='darkblue', fillOpacity=0.2).add_to(m)
folium.GeoJson(shilik_river, fillColor='red', color='darkred', fillOpacity=0.2).add_to(m)

# Save the final map
m.save("130.html")