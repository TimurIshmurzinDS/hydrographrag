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

# 4. Handle coordinates (WKT)
# Note: Context provided entity names but no specific WKT coordinates.
# If coordinates were provided, they would be added here as a hardcoded list.
# Example structure if coordinates existed:
# points = [{"name": "Temirlik village", "coords": [lat, lon]}]
# for pt in points:
#     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

# 5. Save the final map strictly as 86.html
m.save("86.html")