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
folium.GeoJson(data=gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
wkt_coords = [
    {'lat': 48.1234, 'lon': 86.5432},
    {'lat': 47.6543, 'lon': 85.2345}
]

# Add markers to the map using folium.Marker
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Save the final map strictly using a string filename
m.save("158.html")