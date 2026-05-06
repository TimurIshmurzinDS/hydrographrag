import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
water_levels = [
    {'date': '2021-01-01', 'level': 5.6, 'geometry': wkt.loads('POINT(71.4389 -43.2422)')},
    {'date': '2020-01-01', 'level': 5.2, 'geometry': wkt.loads('POINT(71.4389 -43.2422)')}
]

# Add water level points to the map
for level in water_levels:
    folium.CircleMarker(location=[level['geometry'].y, level['geometry'].x], radius=5).add_to(m)

# Save the final map
m.save("122.html")