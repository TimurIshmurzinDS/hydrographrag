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

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
river_coords = [
    {"name": "Аягоз", "wkt": "POINT(71.5439 -48.6072)"},
    {"name": "Токыраун", "wkt": "POINT(72.3456 -49.2345)"}
]

# Add rivers to the map
for river in river_coords:
    folium.Marker(location=tuple(wkt.loads(river['wkt']).xy), popup=river['name']).add_to(m)

# Save the final map
m.save("146.html")