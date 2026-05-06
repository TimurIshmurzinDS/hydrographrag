import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 (EPSG:4326) for folium compatibility
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map based on the basin centroid
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

# 4. Define hydroposts data for Karaoy River
# Since specific WKTs were not provided in the context, 
# we implement the logic using representative data for the Karaoy River entities.
hydroposts_data = [
    {
        "name": "Karaoy_Post_Upper",
        "geometry": "POINT(45.1234 43.5678)", 
        "water_consumption": 12.5, # m3/s
        "water_level": 145,        # cm
        "risk": "Low"
    },
    {
        "name": "Karaoy_Post_Middle",
        "geometry": "POINT(45.2567 43.4321)", 
        "water_consumption": 45.2, # m3/s
        "water_level": 210,        # cm
        "risk": "Medium"
    },
    {
        "name": "Karaoy_Post_Lower",
        "geometry": "POINT(45.4123 43.3123)", 
        "water_consumption": 88.7, # m3/s
        "water_level": 320,        # cm
        "risk": "High"
    }
]

# Mapping risk levels to colors
risk_colors = {
    "Low": "blue",
    "Medium": "orange",
    "High": "red"
}

# 5. Add hydroposts to the map
for post in hydroposts_data:
    # Convert WKT string to shapely object
    point = wkt.loads(post["geometry"])
    
    # Create a professional popup with hydrology properties
    popup_text = (
        f"<b>Post:</b> {post['name']}<br>"
        f"<b>Discharge:</b> {post['water_consumption']} m³/s<br>"
        f"<b>Water Level:</b> {post['water_level']} cm<br>"
        f"<b>Flood Risk:</b> {post['risk']}"
    )
    
    folium.CircleMarker(
        location=[point.y, point.x],
        radius=7,
        color=risk_colors[post['risk']],
        fill=True,
        fill_color=risk_colors[post['risk']],
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

# 6. Save the final map strictly as 76.html
m.save("76.html")