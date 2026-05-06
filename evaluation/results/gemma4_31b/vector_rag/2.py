import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the basin shapefile
# Using 'CartoDB positron' tiles as requested
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Coordinates for sensors (Hardcoded list of dictionaries)
# Note: Context provided entities but no specific WKT coordinates. 
# If coordinates were provided in the context, they would be added here.
sensors_data = [
    # Example structure if coordinates were present:
    # {"name": "Karatal River Sensor", "coords": [lat, lon], "status": "Active"}
]

for sensor in sensors_data:
    folium.Marker(
        location=sensor["coords"],
        popup=f"{sensor['name']}: {sensor['status']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as "2.html"
m.save("2.html")