import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf.to_crs('EPSG:4326', inplace=True)

# Create map
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(gdf.geometry.__geo_interface__, name='basin').add_to(m)
folium.Marker([48.65, 69.5], popup='Лепса', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([49.25, 70.2], popup='Шилик', icon=folium.Icon(color='red')).add_to(m)

# Create hardcoded list of dictionaries
coordinates = [
    {'name': 'Лепса', 'lat': 48.65, 'lon': 69.5},
    {'name': 'Шилик', 'lat': 49.25, 'lon': 70.2}
]

# Add markers to map
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup=coord['name'], icon=folium.Icon(color='blue')).add_to(m)

# Save final map
m.save("152.html")