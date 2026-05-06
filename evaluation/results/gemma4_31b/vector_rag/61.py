import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# Convert to CRS 'EPSG:4326' for compatibility with folium
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
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle sensor coordinates
# Since no WKT coordinates were provided in the context for specific sensors, 
# we proceed with the basin visualization. If coordinates were present, 
# they would be added here as a hardcoded list of dictionaries.
sensors_data = [] # Empty as no WKT provided in context

for sensor in sensors_data:
    folium.Marker(
        location=[sensor['lat'], sensor['lon']],
        popup=f"Sensor: {sensor['name']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 61.html
m.save("61.html")