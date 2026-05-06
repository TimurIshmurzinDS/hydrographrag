import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map with basin boundaries
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.__geo_interface__, name='basin').add_to(m)
m

# Hardcoded list of dictionaries for observations
observations = [
    {'name': '2 км выше устья Проходной реки', 'value': 'выше нормы'},
    {'name': '2 км выше устья Проходной реки', 'value': 'выше нормы'},
    {'name': '2 км выше устья Проходной реки', 'value': 'выше нормы'}
]

# Add observations to map
for obs in observations:
    folium.Marker([obs['lat'], obs['lon']], popup=obs['name'] + ': ' + obs['value']).add_to(m)

# Save final map
m.save("81.html")