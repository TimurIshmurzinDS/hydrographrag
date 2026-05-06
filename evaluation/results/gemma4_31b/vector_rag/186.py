import geopandas as gpd
import folium
from shapely import wkt

# Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326' for compatibility with folium
basin_df = basin_df.to_crs('EPSG:4326')

# Calculate the centroid of the basin to initialize the map center
centroid = basin_df.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

# Initialize folium Map with specified tiles
m = folium.Map(location=[center_lat, center_lon], tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
# Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name='Basin Boundary'
).add_to(m)

# Note: Context provided entities (Butak River, Butak village) but no WKT coordinates.
# If WKT coordinates were provided, they would be added here as folium.Marker.

# Save the final map strictly as 186.html
m.save("186.html")