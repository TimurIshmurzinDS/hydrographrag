import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
# Calculate centroid for centering the map
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin to the map with specified styling
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 4. Handle Observation Entities
# Context mentions "г. Talgar" as an observation point. 
# Since no WKT coordinates were provided in the context, 
# we define the known coordinates for Talgar, Kazakhstan.
observations = [
    {"name": "г. Talgar (Observation)", "lat": 43.2167, "lon": 77.5167}
]

for obs in observations:
    folium.Marker(
        location=[obs["lat"], obs["lon"]],
        popup=obs["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. SAVE the final map strictly using the required filename
m.save("32.html")