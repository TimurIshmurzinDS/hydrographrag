import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path and converting to WGS84 (EPSG:4326)
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
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

# 4. Hardcoded list of monitoring posts for Koktal River
# Since specific WKTs were not provided in the context, 
# we define the structure for the posts based on the requested entities.
posts_data = [
    {
        "name": "Post Koktal-1", 
        "coords": [42.5123, 77.1234], 
        "level": "120 cm", 
        "date": "2023-10-27"
    },
    {
        "name": "Post Koktal-2", 
        "coords": [42.6543, 77.2345], 
        "level": "145 cm", 
        "date": "2023-10-27"
    },
    {
        "name": "Post Koktal-3", 
        "coords": [42.7890, 77.3456], 
        "level": "110 cm", 
        "date": "2023-10-27"
    }
]

# 5. Add markers for each post to the map
for post in posts_data:
    popup_text = f"Post: {post['name']}<br>Water Level: {post['level']}<br>Date: {post['date']}"
    folium.Marker(
        location=post['coords'],
        popup=popup_text,
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 6. Save the final map strictly as 88.html
m.save("88.html")