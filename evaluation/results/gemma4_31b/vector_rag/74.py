import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = basin_df.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium Map with CartoDB positron tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# Note: The context provides descriptions of observation points ("2 km above mouth"), 
# but no specific WKT coordinates were provided. 
# If coordinates were available, they would be added here as a hardcoded list of dictionaries.

# Save the final map strictly as 74.html
m.save("74.html")