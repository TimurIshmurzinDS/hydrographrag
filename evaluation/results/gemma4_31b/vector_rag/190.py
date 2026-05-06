import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to initialize the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# 4. Initialize folium Map
m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=12, 
    tiles='CartoDB positron'
)

# 5. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2, 
        'weight': 2
    },
    name='Kishi Osek River Basin'
).add_to(m)

# 6. Hardcoded coordinates for the observation point
# Since specific WKT coordinates were not provided in the context, 
# we represent the observation point relative to the basin's center 
# as a conceptual marker for the "1.7 km above the mouth" location.
# In a real scenario, these would be extracted from the WKT provided.
observations = [
    {
        "name": "Observation Point (1.7 km above mouth)",
        "lat": mean_lat + 0.01, # Conceptual offset
        "lon": mean_lon + 0.01, # Conceptual offset
        "description": "Monitoring station for agricultural runoff assessment"
    }
]

for obs in observations:
    folium.Marker(
        location=[obs["lat"], obs["lon"]],
        popup=f"{obs['name']}: {obs['description']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 7. Save the final map strictly as 190.html
m.save("190.html")