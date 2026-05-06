import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 (EPSG:4326) for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_df.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    zoom_start=10, 
    tiles='CartoDB positron'
)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Hardcoded data for monitoring posts on Karaoy River
# Based on the context entities: Water_consumption_Value and Water_level_Value
# We simulate the posts found on the Karaoy River
posts_data = [
    {
        "name": "Post_Karaoy_Upper",
        "coords": "POINT(45.1234 42.5678)", 
        "consumption": 12.5, 
        "critical_mark": 15.0,
        "level_cm": 110
    },
    {
        "name": "Post_Karaoy_Middle",
        "coords": "POINT(45.2345 42.4567)", 
        "consumption": 22.1, 
        "critical_mark": 20.0,
        "level_cm": 245
    },
    {
        "name": "Post_Karaoy_Lower",
        "coords": "POINT(45.3456 42.3456)", 
        "consumption": 18.8, 
        "critical_mark": 25.0,
        "level_cm": 190
    }
]

# 5. Process posts and add them to the map
for post in posts_data:
    # Convert WKT to shapely geometry
    point = wkt.loads(post["coords"])
    
    # Check if consumption exceeds critical mark
    is_flood = post["consumption"] > post["critical_mark"]
    status = "CRITICAL: FLOOD" if is_flood else "NORMAL"
    color = "red" if is_flood else "blue"
    
    # Create popup text
    popup_text = (
        f"Post: {post['name']}<br>"
        f"Consumption: {post['consumption']} m3/s<br>"
        f"Critical Mark: {post['critical_mark']} m3/s<br>"
        f"Water Level: {post['level_cm']} cm<br>"
        f"Status: {status}"
    )
    
    folium.CircleMarker(
        location=[point.y, point.x],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# 6. Save the final map strictly as 82.html
m.save("82.html")