import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the folium map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]

m = folium.Map(
    location=map_center, 
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

# 4. Handle Coordinates (WKT)
# Based on the provided context, no specific WKT coordinates were given.
# If coordinates were present, they would be added here as a hardcoded list of dictionaries.
# Example structure if data existed:
# points_data = [{"loc": [lat, lon], "info": "Consumption Value"}]
# for point in points_data:
#     folium.Marker(location=point["loc"], popup=point["info"]).add_to(m)

# 5. Save the final map strictly as "45.html"
m.save("45.html")