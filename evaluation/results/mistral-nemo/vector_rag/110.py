import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'name': 'Sarykan River', 'wkt': 'POINT(74.56 -39.12)'},
    {'name': 'Tekeli River', 'wkt': 'POINT(75.89 -38.76)'}
]

# Add points to the map
for coord in coordinates:
    folium.Marker(wkt.loads(coord['wkt']), popup=coord['name']).add_to(m)

# Save the final map as "110.html"
m.save("110.html")