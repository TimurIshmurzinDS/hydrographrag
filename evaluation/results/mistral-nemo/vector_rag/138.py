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

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
river_lepsy = {"type": "Feature", "geometry": wkt.loads('POINT(74.561389 42.866667)'), "properties": {"name": "Лепсы"}}
river_butak = {"type": "Feature", "geometry": wkt.loads('POINT(74.500000 42.833333)'), "properties": {"name": "Бутак"}}

# Add rivers to the map
for river in [river_lepsy, river_butak]:
    folium.GeoJson(
        data=river,
        style_function=lambda x: {'color': 'blue', 'weight': 2},
    ).add_to(m)

# Save the final map
m.save("138.html")