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
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {"type": "Feature", "geometry": wkt.loads("POINT (-74.0060 4.5703)"), "properties": {"name": "Emel River"}},
    {"type": "Feature", "geometry": wkt.loads("POINT (-72.8913 4.2146)"), "properties": {"name": "Sarykan River"}}
]

# Add rivers to the map
for river in coordinates:
    folium.GeoJson(
        river,
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.8},
    ).add_to(m)

# Save the final map
m.save("168.html")