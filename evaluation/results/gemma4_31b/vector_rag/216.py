import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Hardcoded sensor data based on the provided entities
# Since coordinates were not provided in the context, we simulate sensor points 
# within the vicinity of the Karaoy River basin.
sensors_data = [
    {
        "id": "WB_KARAOY_01", 
        "name": "Sensor Alpha", 
        "coords": [centroid.y + 0.02, centroid.x + 0.02], 
        "level": "1.25m", 
        "date": "2023-10-27"
    },
    {
        "id": "WB_KARAOY_02", 
        "name": "Sensor Beta", 
        "coords": [centroid.y - 0.03, centroid.x - 0.01], 
        "level": "0.98m", 
        "date": "2023-10-27"
    }
]

# 5. Add sensors to the map to enable "teleportation" (navigation)
for sensor in sensors_data:
    folium.Marker(
        location=sensor["coords"],
        popup=f"ID: {sensor['id']}<br>Level: {sensor['level']}<br>Date: {sensor['date']}",
        tooltip=sensor["name"],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 6. Save the final map strictly as 216.html
m.save("216.html")