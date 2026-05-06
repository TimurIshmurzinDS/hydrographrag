import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
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
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# 4. Handle coordinates if provided in context (WKT)
# Note: Context provided entity names but no specific WKT coordinates.
# If coordinates were present, they would be added here as a list of dictionaries.
river_points = [] # Empty as no WKT provided in context

for point in river_points:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=point['name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 5. Save the final map strictly as 85.html
m.save("85.html")