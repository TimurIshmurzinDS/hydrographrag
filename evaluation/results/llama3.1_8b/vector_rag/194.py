import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
coordinates = [
    {'lat': 43.1234, 'lon': 72.3456},
    {'lat': 43.2345, 'lon': 72.4567}
]

# Add markers to the map using folium.Marker
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# SAVE the final map: m.save("194.html")
m.save("194.html")