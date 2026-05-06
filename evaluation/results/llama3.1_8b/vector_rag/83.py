import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(data=gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
wkt_coords = [
    {'lat': 48.1234, 'lon': 77.5678},
    {'lat': 48.2345, 'lon': 78.9012}
]

# Add markers to the map using folium.Marker
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Marker').add_to(m)

# Save the final map strictly using a string filename
m.save("83.html")