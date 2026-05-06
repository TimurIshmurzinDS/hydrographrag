import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
centroid = gdf.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Create a hardcoded list of dictionaries for observations
observations = [
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.123456, 'lon': 76.789012}
]

# Add observations to the map
for obs in observations:
    folium.Marker([obs['lat'], obs['lon']], icon=folium.Icon(color='red')).add_to(m)

# Save the final map
m.save("15.html")