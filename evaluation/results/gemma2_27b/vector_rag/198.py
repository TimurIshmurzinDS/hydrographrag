import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basins = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize the map centered on the centroid of the basins
m = folium.Map(location=basins.centroid.values[0], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basins, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Save the map
m.save("198.html")