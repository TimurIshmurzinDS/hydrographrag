import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(gdf.geometry.__geo_interface__, name='basin').add_to(m)

# Create hardcoded list of dictionaries for observations
observations = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.1245, 'lon': 76.5443},
    {'lat': 43.1256, 'lon': 76.5454},
    {'lat': 43.1267, 'lon': 76.5465}
]

# Add observations to map
for obs in observations:
    folium.Marker(location=[obs['lat'], obs['lon']], icon=folium.Icon(color='red')).add_to(m)

# Save final map
m.save("16.html")