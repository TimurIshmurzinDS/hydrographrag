import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If there are coordinates (WKT), create a hardcoded list of dictionaries
water_level_points = [
    {'date': '2017-01-01', 'value_cm': 50, 'geometry': wkt.loads('POINT(37.4698 -122.2419)')},
    {'date': '2017-02-01', 'value_cm': 55, 'geometry': wkt.loads('POINT(37.4698 -122.2419)')}
]

# Add water level points to the map
for point in water_level_points:
    folium.CircleMarker(location=[point['geometry'].y, point['geometry'].x], radius=5).add_to(m)

# Save the final map
m.save("50.html")