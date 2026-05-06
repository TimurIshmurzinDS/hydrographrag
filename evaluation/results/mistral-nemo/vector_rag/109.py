import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(gdf, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
byzhy_river = {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(53.1234 78.9012)'), 'properties': {}, 'type': 'Feature'}]}
lepsy_river = {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(54.5678 79.3456)'), 'properties': {}, 'type': 'Feature'}]}

# Add rivers to the map
folium.GeoJson(byzhy_river, fillColor='blue', color='darkblue', fillOpacity=0.2).add_to(m)
folium.GeoJson(lepsy_river, fillColor='red', color='darkred', fillOpacity=0.2).add_to(m)

# Save the final map
m.save("109.html")