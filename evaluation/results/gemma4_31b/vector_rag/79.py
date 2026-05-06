import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile strictly using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize folium.Map using the centroid of the basin polygon
# Using 'CartoDB positron' tiles as requested
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
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

# 4. Coordinates handling
# The context provided does not contain specific WKT coordinates for the rivers or observations.
# If coordinates were provided, they would be added here as a hardcoded list of dictionaries.
# Example structure (commented out):
# points = [{"name": "Turgen River Obs", "coords": [lat, lon]}]
# for pt in points:
#     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

# 5. Save the final map strictly as "79.html"
m.save("79.html")