import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt).add_to(m)

# Create a hardcoded list of dictionaries for Coordinates (WKT) if available
coordinates = [
    {'name': 'Shilik River', 'wkt': wkt.loads('POINT(48.123 77.456)')},
    {'name': 'Shyzhyn River', 'wkt': wkt.loads('POINT(49.789 78.321)')}
]

# Add markers for each river
for coord in coordinates:
    folium.Marker(location=coord['wkt'].coords[0], popup=coord['name']).add_to(m)

# SAVE the final map: m.save("157.html")
m.save("157.html")