import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile
# Using raw string for path as per instructions
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
gdf = gdf.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Handle coordinates (WKT)
# Context does not provide specific WKT coordinates for the rivers or observation points.
# If coordinates were provided, they would be added here as a hardcoded list of dictionaries.
points_to_plot = [] 

for point in points_to_plot:
    folium.Marker(
        location=[point['lat'], point['lon']], 
        popup=point['name']
    ).add_to(m)

# 5. Save the final map strictly as 11.html
m.save("11.html")