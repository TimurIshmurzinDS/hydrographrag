import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {"name": "Il River", "wkt": "POINT(74.56 43.29)"},
    {"name": "Karatal River", "wkt": "POINT(70.18 43.25)"}
]

# Process coordinates and add them to the map
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker(location=tuple(point.coords[0]), popup=coord['name']).add_to(m)

# Save the final map
m.save("150.html")