import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
observations = [
    {"type": "Feature", "geometry": wkt.loads("POINT(53.123456 -78.987654)"), "properties": {"Date_water_level_Value": 0.2}},
    {"type": "Feature", "geometry": wkt.loads("POINT(53.234567 -78.876543)"), "properties": {"Date_water_level_Value": 0.2}}
]

# Add observations to the map
for obs in observations:
    folium.CircleMarker(
        location=[obs['geometry'].y, obs['geometry'].x],
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"Date_water_level_Value: {obs['properties']['Date_water_level_Value']}"
    ).add_to(m)

# Save the final map
m.save("220.html")