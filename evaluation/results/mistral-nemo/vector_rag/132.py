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
lepsy_river = [{'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(51.5074 -0.1278)'), 'properties': {'Date_water_level_Value': 2015}}, {'geometry': wkt.loads('POINT(51.5074 -0.1278)'), 'properties': {'Date_water_level_Value': 2016}}]}]
tekes_river = [{'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(51.5074 -0.1278)'), 'properties': {'Water_level_Value': 2015}}, {'geometry': wkt.loads('POINT(51.5074 -0.1278)'), 'properties': {'Water_level_Value': 2016}}]}]

# Add rivers to the map
for river in lepsy_river:
    folium.GeoJson(
        data=river,
        style_function=lambda x: {'fillColor': 'blue', 'color': 'darkblue', 'fillOpacity': 0.5},
    ).add_to(m)

for river in tekes_river:
    folium.GeoJson(
        data=river,
        style_function=lambda x: {'fillColor': 'red', 'color': 'darkred', 'fillOpacity': 0.5},
    ).add_to(m)

# Save the final map
m.save("132.html")