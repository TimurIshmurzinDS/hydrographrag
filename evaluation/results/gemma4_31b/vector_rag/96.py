import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium Map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
center_lat = centroid.y.mean()
center_lon = centroid.x.mean()

m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
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

# 4. Handle Coordinates (WKT)
# Based on the context, specific WKT coordinates were not provided.
# If they were present, they would be added here as a hardcoded list of dictionaries.
points_of_interest = [] 
# Example structure if coordinates were available:
# points_of_interest = [
#     {"name": "Urzhar Point 1", "coords": [lat1, lon1]},
#     {"name": "Dos Point 1", "coords": [lat2, lon2]}
# ]

for point in points_of_interest:
    folium.Marker(
        location=point["coords"], 
        popup=point["name"], 
        icon=folium.Icon(color='blue')
    ).add_to(m)

# 5. Save the final map strictly as 96.html
m.save("96.html")