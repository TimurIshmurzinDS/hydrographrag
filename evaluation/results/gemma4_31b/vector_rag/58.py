import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the shapefile
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
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Coordinates handling
# Since no specific WKT coordinates for Sarykan River were provided in the context, 
# we focus on the basin boundary. If coordinates were present, they would be added here.
# Example of how a hardcoded list would be implemented if WKT existed:
# points = [{"name": "Sarykan Station", "coords": [lat, lon]}]
# for p in points:
#     folium.Marker([p["coords"][0], p["coords"][1]], popup=p["name"]).add_to(m)

# 5. Save the final map strictly using the required filename
m.save("58.html")