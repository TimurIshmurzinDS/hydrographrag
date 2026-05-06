import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates in WKT format, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT (43.6159 -79.4514)'), 'properties': {}}]}
]

# Add the coordinates to the map
for coord in coordinates:
    folium.GeoJson(coord).add_to(m)

# Save the final map
m.save("246.html")