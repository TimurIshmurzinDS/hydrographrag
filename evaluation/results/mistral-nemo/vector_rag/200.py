import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    basin,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
observations = [
    {"type": "Observation", "geometry": wkt.loads("POINT(1.7 km above the mouth of Kishi Osek River)")} for _ in range(4)
]

# Add observations to the map
for obs in observations:
    folium.CircleMarker(
        location=tuple(obs['geometry'].coords.xy),
        radius=5,
        color='red',
    ).add_to(m)

# Save the final map
m.save("200.html")