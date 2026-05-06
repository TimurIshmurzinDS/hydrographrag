import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(data=gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for points
points = [
    {'name': 'Темирлик village', 'lat': 48.1234, 'lon': 69.5678},
]

# Add points to the map
for point in points:
    folium.Marker([point['lat'], point['lon']], popup=point['name']).add_to(m)

# Create a hardcoded list of dictionaries for rivers
rivers = [
    {'name': 'Karaoy River', 'lat': 48.1234, 'lon': 69.5678},
    {'name': 'Temirlik River', 'lat': 48.9012, 'lon': 70.2345},
    {'name': 'Turgen River', 'lat': 49.0123, 'lon': 71.3456},
]

# Add rivers to the map
for river in rivers:
    folium.Marker([river['lat'], river['lon']], popup=river['name']).add_to(m)

# Save the final map
m.save("86.html")