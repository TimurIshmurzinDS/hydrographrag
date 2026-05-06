import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
kishi_almaty_river = [{'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(71.45 43.25)'), 'properties': {}, 'type': 'Feature'}]}]

# Add the river to the map
folium.GeoJson(kishi_almaty_river, fillColor='blue', color='blue', fillOpacity=0.8).add_to(m)

# Save the final map
m.save("225.html")