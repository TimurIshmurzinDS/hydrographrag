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

# If there are Coordinates (WKT) in the context, create a hardcoded list of dictionaries
observations = [
    {"type": "Feature", "geometry": wkt.loads('POINT(12.3456789 98.7654321)', srs='EPSG:4326'), "properties": {"name": "0.2 km above confluence with Osek River"}},
    # Add more observations as needed
]

# Add observations to the map
for obs in observations:
    folium.CircleMarker(
        location=tuple(obs['geometry'].coords),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.5,
    ).add_to(m)

# Save the final map
m.save("238.html")