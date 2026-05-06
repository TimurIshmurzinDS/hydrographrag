import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium map centered on the basin centroid
m = folium.Map(location=basin.centroid.values[0], tiles='CartoDB positron', zoom_start=10)

# Add the basin to the map
folium.GeoJson(data=basin, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If coordinates (WKT) are available in the context, add them as markers
# Example:
coordinates = [
    {'geometry': wkt.loads('POINT (55.7 37.6)'), 'label': 'Butak village'},
]
for coord in coordinates:
    folium.Marker(location=[coord['geometry'].y, coord['geometry'].x], popup=coord['label']).add_to(m)

# Save the map
m.save("192.html")