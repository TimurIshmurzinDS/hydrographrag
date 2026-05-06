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
rivers = [
    {"name": "Sarykan River", "geometry": wkt.loads("POINT(74.56 41.34)")},
    {"name": "Temirlik River", "geometry": wkt.loads("POINT(74.89 40.92)")}
]

# Add rivers to the map
for river in rivers:
    folium.Marker(location=river['geometry']).add_to(m)

# Save the final map
m.save("118.html")