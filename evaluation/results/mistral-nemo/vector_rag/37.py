import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If WKT coordinates are not provided, create them manually as a list of dictionaries
kumbel_river_coords = [
    {'type': 'Point', 'coordinates': [long1, lat1]},
    {'type': 'Point', 'coordinates': [long2, lat2]}
]

# Add Kumbel River to the map using hardcoded coordinates
for coord in kumbel_river_coords:
    folium.Marker(wkt.loads(coord['type'] + '(' + ','.join(map(str, coord['coordinates'])) + ')')).add_to(m)

# Save the final map
m.save("37.html")