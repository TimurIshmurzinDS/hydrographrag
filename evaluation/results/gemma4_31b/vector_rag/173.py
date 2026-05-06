import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# 2. Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# 3. Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# 4. Initialize folium Map
# Using 'CartoDB positron' tiles as requested
m = folium.Map(location=map_center, zoom_start=10, tiles='CartoDB positron')

# 5. Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Basin Boundary"
).add_to(m)

# Note: No WKT coordinates were provided in the context for the Shynzhaly River,
# so no hardcoded point markers are added. The map focuses on the basin context.

# 6. Save the final map strictly as "173.html"
m.save("173.html")