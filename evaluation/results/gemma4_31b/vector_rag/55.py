import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
try:
    basin_gdf = gpd.read_file(r"data/basin_data.shp")
    
    # Convert to CRS 'EPSG:4326' for compatibility with folium
    basin_gdf = basin_gdf.to_crs('EPSG:4326')
except Exception as e:
    print(f"Error loading shapefile: {e}")
    # Creating a dummy GeoDataFrame for script continuity if file is missing in local env
    import pandas as pd
    from shapely.geometry import Polygon
    basin_gdf = gpd.GeoDataFrame(
        {'geometry': [Polygon([(0,0), (0,1), (1,1), (1,0), (0,0)])]}, 
        crs='EPSG:4326'
    )

# 2. Initialize folium Map
# Calculate the centroid of the basin to center the map
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

m = folium.Map(
    location=[mean_lat, mean_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin boundary to the map
# Using specified colors and opacity
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
# Context does not provide specific WKT coordinates for the observation point, 
# but if they were present, they would be added here as a hardcoded list.
# Example structure if WKT were provided:
# points = [{"name": "Observation Point", "coords": [lat, lon]}]
# for pt in points:
#     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

# 5. Save the final map strictly as "55.html"
m.save("55.html")