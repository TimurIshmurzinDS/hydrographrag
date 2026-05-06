import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

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
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Coordinates for monitoring points (if provided in context as WKT)
# Since no specific WKT coordinates were provided in the context for Observation_1, 
# we focus on the basin visualization. If coordinates were present, they would be added here.
monitoring_points = [] 

for point in monitoring_points:
    folium.Marker(
        location=[point['lat'], point['lon']], 
        popup=point['name']
    ).add_to(m)

# 5. Save the final map strictly as 14.html
m.save("14.html")