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
observations = [
    {"type": "Feature", "geometry": wkt.loads("POINT(1.7 km above the mouth of Kishi Osek River)"), "properties": {"name": "Observation 1"}},
    # Add more observations if needed
]

# Add observations to the map
for obs in observations:
    folium.Marker(location=tuple(obs['geometry'].coords[0]), popup=obs['properties']['name']).add_to(m)

# Save the final map
m.save("179.html")