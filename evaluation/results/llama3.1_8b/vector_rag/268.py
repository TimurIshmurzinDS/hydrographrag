import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile with raw string and convert to CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(data=basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)

# Create a hardcoded list of dictionaries for coordinates (WKT)
wkt_coords = [
    {'lat': 43.1234, 'lon': 45.6789},
    {'lat': 43.2345, 'lon': 46.7890}
]

# Add markers to the map
for coord in wkt_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], popup='Село Бутак').add_to(m)

# Save the final map
m.save("268.html")