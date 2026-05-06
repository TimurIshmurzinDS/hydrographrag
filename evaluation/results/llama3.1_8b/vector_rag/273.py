import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile strictly using a raw string
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile and parameter tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson (fillColor='green', color='darkgreen', fillOpacity=0.2)
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Create a hardcoded list of dictionaries for Coordinates (WKT)
wkt_coords = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(76.2345 46.7890)')},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(77.1234 47.5678)')}
]

# Add markers to the map
for coord in wkt_coords:
    folium.Marker(location=coord['geometry'].coords[0], popup='Marker').add_to(m)

# SAVE the final map: m.save("273.html")
m.save("273.html")