import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
centroid = gdf.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.__geo_interface__, name='Basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
coordinates = [
    {'lat': 46.1234, 'lon': 68.9012},
    {'lat': 47.2345, 'lon': 69.0123}
]

# Add markers to the map
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Save the final map
m.save("114.html")