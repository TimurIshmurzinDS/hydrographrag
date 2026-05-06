import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the shapefile using a raw string
# The file data/basin_data.shp contains only the exterior polygon boundaries of the basin
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# 2. Convert to CRS 'EPSG:4326'
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin for map initialization
centroid = basin_gdf.geometry.centroid.iloc[0]
center_lat = centroid.y
center_lon = centroid.x

# 4. Initialize folium.Map using the centroid and CartoDB positron tiles
m = folium.Map(
    location=[center_lat, center_lon], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 5. Add the basin to the map using folium.GeoJson
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    tooltip="Basin of Kumbel River"
).add_to(m)

# Note: Context does not provide WKT coordinates for specific points, 
# so no hardcoded point dictionaries are added.

# 6. Save the final map strictly using the required filename
m.save("233.html")