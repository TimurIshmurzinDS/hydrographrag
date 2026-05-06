import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile with raw string and convert to CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT) if available
coordinates = [
    {'lat': 48.6734, 'lon': 68.7363},
    {'lat': 48.6745, 'lon': 68.7372}
]

# Add markers to the map using folium.Marker
for coord in coordinates:
    folium.Marker([coord['lat'], coord['lon']], popup='Marker').add_to(m)

# Save the final map strictly using a string filename: m.save("135.html")
m.save("135.html")