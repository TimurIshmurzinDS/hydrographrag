import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Create map with basin
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.geometry.__geo_interface__, name='basin', color='darkgreen', fillOpacity=0.2).add_to(m)

# Create hardcoded list of dictionaries with WKT coordinates
wkt_coords = [
    {'lat': 43.1234, 'lon': 76.5432},
    {'lat': 43.1245, 'lon': 76.5443},
    {'lat': 43.1256, 'lon': 76.5454}
]

# Add WKT coordinates to map
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Save final map
m.save("225.html")