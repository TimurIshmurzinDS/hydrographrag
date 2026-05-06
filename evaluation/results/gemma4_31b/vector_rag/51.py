import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map
# Use the centroid of the basin polygon to center the map
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]

m = folium.Map(
    location=map_center, 
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

# 4. Coordinates for Kurty River (if provided in context as WKT)
# Since no specific WKT coordinates were provided in the context for the river points,
# we proceed with the basin visualization. If coordinates were present, 
# they would be added here as a list of dictionaries.
river_points = [] 
for point in river_points:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as "51.html"
m.save("51.html")