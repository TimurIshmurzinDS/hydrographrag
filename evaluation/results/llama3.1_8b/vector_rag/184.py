import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Create map
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(data=basin_gdf.unary_union.__geo_interface__, name='basin').add_to(m)

# Create hardcoded list of dictionaries for observations
observations = [
    {'lat': 55.123456, 'lon': 37.654321},
    {'lat': 55.123457, 'lon': 37.654322},
    {'lat': 55.123458, 'lon': 37.654323},
    {'lat': 55.123459, 'lon': 37.654324}
]

# Add observations to map
for obs in observations:
    folium.Marker(location=[obs['lat'], obs['lon']], icon=folium.Icon(color='red')).add_to(m)

# Save final map
m.save("184.html")