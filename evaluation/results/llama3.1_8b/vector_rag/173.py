import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Create a hardcoded list of dictionaries for Coordinates (WKT)
coordinates = [
    {'lat': 43.1234, 'lon': 79.5678},
    {'lat': 43.2345, 'lon': 80.6789}
]

# Add markers to the map
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']]).add_to(m)

# Save the final map
m.save("173.html")