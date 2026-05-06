import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Hardcoded list of sensors (Coordinates were not provided in context, 
# but structure is maintained for professional implementation)
sensors = [
    # Example structure if WKT were present:
    # {"name": "Sensor 1 (г. Talgar)", "geometry": wkt.loads("POINT(lon lat)")},
]

for sensor in sensors:
    coords = [sensor["geometry"].y, sensor["geometry"].x]
    folium.Marker(
        location=coords, 
        popup=sensor["name"], 
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 10.html
m.save("10.html")