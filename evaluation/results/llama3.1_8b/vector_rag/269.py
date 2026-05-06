import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'lat': 37.7749, 'lon': -122.4194},
    {'lat': 38.8977, 'lon': -77.0365}
]

# Add markers to the map
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Marker').add_to(m)

# Save the final map
m.save("269.html")