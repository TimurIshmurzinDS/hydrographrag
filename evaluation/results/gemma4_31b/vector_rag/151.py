import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# Convert to WGS84 (EPSG:4326) for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map
# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
# Strictly following the style requirements: green fill, darkgreen border, 0.2 opacity
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

# 4. Handle coordinates from context
# The context mentions Bayankol River, Ili River, and Bayankol village.
# Since no specific WKT coordinates were provided in the prompt text, 
# we define the logic for adding them if they were present.
# Example of how hardcoded points would be added if WKT existed:
# points_data = [
#     {"name": "Bayankol village", "geometry": "POINT(lon lat)"},
#     {"name": "Ili River Point", "geometry": "POINT(lon lat)"}
# ]
# for pt in points_data:
#     geom = wkt.loads(pt["geometry"])
#     folium.Marker([geom.y, geom.x], popup=pt["name"]).add_to(m)

# 5. Save the final map strictly as 151.html
m.save("151.html")