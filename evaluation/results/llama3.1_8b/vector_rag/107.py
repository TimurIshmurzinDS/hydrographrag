import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Create map
m = folium.Map(location=[basin_gdf.centroid.y, basin_gdf.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Add basin to map
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt), name='basin').add_to(m)

# Create hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'name': 'Temirlik village', 'wkt': wkt.loads('POINT(77.2345 42.3456)')},
    {'name': 'Tekeli River', 'wkt': wkt.loads('LINESTRING(77.1234 42.5678, 78.9012 43.4567)')}
]

# Add coordinates to map
for coord in coordinates:
    folium.Marker([coord['wkt'].coords[0][1], coord['wkt'].coords[0][0]], popup=coord['name']).add_to(m)

# Save final map
m.save("107.html")