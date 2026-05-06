import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map with specified tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 5. Add the basin boundary to the map with strict styling
folium.GeoJson(
    basin_gdf,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2
).add_to(m)

# 6. Hardcoded coordinates for sensors on Ayagoz and Tokyraun rivers
# Since WKT coordinates were not provided in the context, 
# we define a representative list for the requested rivers.
sensors_data = [
    {"name": "Sensor_Ayagoz_01", "lat": 49.1234, "lon": 78.5678, "status": "Check Required"},
    {"name": "Sensor_Tokyraun_01", "lat": 49.4321, "lon": 78.8765, "status": "Check Required"}
]

# Add sensor markers to the map
for sensor in sensors_data:
    folium.Marker(
        location=[sensor["lat"], sensor["lon"]],
        popup=f"{sensor['name']} - {sensor['status']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# 7. Save the final map strictly as 146.html
m.save("146.html")