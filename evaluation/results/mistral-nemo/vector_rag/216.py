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
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
coordinates = [
    {'type': 'FeatureCollection', 'features': [{'geometry': wkt.loads('POINT(49.123456 40.123456)', srid=4326), 'properties': {'Water_body_code': 'KAROY1', 'Water_level_Value': 123, 'Date_water_level_Value': '2022-01-01'}}, {'geometry': wkt.loads('POINT(49.654321 40.654321)', srid=4326), 'properties': {'Water_body_code': 'KAROY2', 'Water_level_Value': 234, 'Date_water_level_Value': '2022-02-15'}}]}
]

# Add coordinates to the map using folium.CircleMarker
for coord in coordinates:
    folium.CircleMarker(
        location=coord['features'][0]['geometry'].coords,
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f'Water body code: {coord["properties"]["Water_body_code"]}<br>Water level value: {coord["properties"]["Water_level_Value"]} m<br>Date of water level measurement: {coord["properties"]["Date_water_level_Value"]}'
    ).add_to(m)

# Save the final map
m.save("216.html")