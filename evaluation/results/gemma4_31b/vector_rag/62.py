import geopandas as gpd
import folium
from shapely import wkt

# Load the basin boundary shapefile
# Using raw string for path as per instructions
gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 coordinate system
gdf = gdf.to_crs('EPSG:4326')

# Calculate the centroid of the basin to center the map
centroid = gdf.geometry.centroid
center_lat = centroid.y.iloc[0]
center_lon = centroid.x.iloc[0]

# Initialize the folium map with CartoDB positron tiles
m = folium.Map(location=[center_lat, center_lon], 
               tiles='CartoDB positron', 
               zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# The context mentions "below the mouth of Sarysai River" but provides no WKT coordinates.
# If coordinates were provided in the context, they would be added here as a list of dictionaries.
monitoring_posts = []

# Add markers for monitoring posts if any were found in context
for post in monitoring_posts:
    folium.Marker(
        location=[post['lat'], post['lon']],
        popup=post['name'],
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Save the final map strictly as 62.html
m.save("62.html")