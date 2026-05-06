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

# Hardcoded list of dictionaries containing coordinates (WKT) for rivers with water level anomalies
rivers_with_anomalies = [
    {"name": "Sarykan River", "geometry": wkt.loads("POINT(45.123 78.901)")},
    # Add more rivers as needed
]

# Add rivers with anomalies to the map (red color)
for river in rivers_with_anomalies:
    folium.GeoJson(
        data=[river],
        style_function=lambda x: {'fillColor': 'red', 'color': 'darkred', 'fillOpacity': 0.2},
    ).add_to(m)

# Save the final map
m.save("139.html")