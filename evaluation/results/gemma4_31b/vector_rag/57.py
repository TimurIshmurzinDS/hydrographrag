import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326'
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid for map initialization
centroid = basin_gdf.geometry.centroid
mean_lat = centroid.y.mean()
mean_lon = centroid.x.mean()

# 4. Initialize folium Map
m = folium.Map(
    location=[mean_lat, mean_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 5. Add the basin boundary to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# Note: No WKT coordinates were provided in the context for specific river points,
# so only the basin boundary is visualized.

# 6. Save the final map strictly as 57.html
m.save("57.html")