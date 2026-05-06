import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string and convert to CRS 'EPSG:4326'
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Calculate the centroid of the basin for map initialization
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# 3. Initialize folium Map with specified tiles
m = folium.Map(
    location=[mean_lat, mean_lon], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 4. Add the basin boundary to the map
# Using strict styling: fillColor='green', color='darkgreen', fillOpacity=0.2
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

# 5. Coordinates handling
# The context provided entities but no specific WKT coordinates. 
# If WKT coordinates were provided, they would be added here as a hardcoded list.
# Example structure (commented out as no WKT provided in context):
# points = [
#     {"name": "Sarykan River", "coords": [lat, lon]},
#     {"name": "Tekeli River", "coords": [lat, lon]}
# ]
# for pt in points:
#     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

# 6. Save the final map strictly as "110.html"
m.save("110.html")