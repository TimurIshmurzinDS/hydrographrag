import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
tentek_river = {'type': 'HY_HydroFeature', 'name': 'Тентек', 'geometry': wkt.loads('POINT(51.5074 719.9928)')}
byzhy_river = {'type': 'HY_HydroFeature', 'name': 'Быж', 'geometry': wkt.loads('POINT(51.6032 720.1234)')}

# Add rivers to the map using folium.CircleMarker
folium.CircleMarker(location=[tentek_river['geometry'].y, tentek_river['geometry'].x], radius=5, color='blue').add_to(m)
folium.CircleMarker(location=[byzhy_river['geometry'].y, byzhy_river['geometry'].x], radius=5, color='red').add_to(m)

# Save the final map
m.save("94.html")