import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326'
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=8, 
    tiles='CartoDB positron'
)

# 3. Add the basin to the map with specific styling
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Define coordinates for the entities
# Note: Orion is an astronomical object; we use a hypothetical terrestrial projection point.
# Shilik River point is based on the observation location (0.2 km above confluence with Osek).
locations = [
    {"name": "Orion Projection", "coords": [43.5, 78.0]}, 
    {"name": "Shilik River Observation Point", "coords": [44.2, 82.5]}
]

# Add markers and create the path
points = []
for loc in locations:
    folium.Marker(
        location=loc["coords"], 
        popup=loc["name"], 
        icon=folium.Icon(color='blue' if "Shilik" in loc["name"] else 'orange')
    ).add_to(m)
    points.append(loc["coords"])

# Draw the shortest path (straight line) between Orion and Shilik River
folium.PolyLine(
    locations=points, 
    color='red', 
    weight=2.5, 
    opacity=0.8, 
    tooltip="Shortest Path: Orion -> Shilik River"
).add_to(m)

# 5. Save the final map strictly as 246.html
m.save("246.html")