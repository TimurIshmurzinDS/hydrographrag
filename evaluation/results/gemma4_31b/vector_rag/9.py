import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=6, 
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
    }
).add_to(m)

# 4. Hardcoded coordinates for entities if WKT were provided. 
# Since no WKT coordinates were provided in the context, 
# we only visualize the basin boundary.
# Example structure if coordinates existed:
# points = [{"name": "Ili River", "coords": [lat, lon]}, ...]
# for pt in points:
#     folium.Marker([pt['coords'][0], pt['coords'][1]], popup=pt['name']).add_to(m)

# 5. Save the final map strictly as "9.html"
m.save("9.html")