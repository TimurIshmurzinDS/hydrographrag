import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile
# The file contains only the exterior polygon boundaries of the basin
basin_path = r"data/basin_data.shp"
basin_df = gpd.read_file(basin_path)

# Convert to WGS84 CRS for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_df.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# 3. Add the basin boundary to the map
folium.GeoJson(
    basin_df,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Lepsi River Basin"
).add_to(m)

# 4. Hardcoded data points representing monitoring stations and irrigation points
# Since WKT coordinates were not provided in the context, we simulate 
# representative points within the Lepsi river region to demonstrate the influence.
monitoring_data = [
    {
        "location": "POINT(79.1234 43.5678)", 
        "quality": "Class 2 (Good)", 
        "consumption": "150 m³s", 
        "level": "1.2m",
        "desc": "Upper Reach - Low Ag Influence"
    },
    {
        "location": "POINT(79.4567 43.4321)", 
        "quality": "Class 4 (Poor)", 
        "consumption": "450 m³s", 
        "level": "0.8m",
        "desc": "Middle Reach - High Ag Influence"
    },
    {
        "location": "POINT(79.8765 43.3100)", 
        "quality": "Class 3 (Fair)", 
        "consumption": "300 m³s", 
        "level": "1.0m",
        "desc": "Lower Reach - Moderate Ag Influence"
    }
]

# 5. Add points to the map
for point in monitoring_data:
    # Convert WKT string to shapely geometry
    geom = wkt.loads(point["location"])
    
    # Create a popup text detailing the entities
    popup_text = (
        f"<b>Status:</b> {point['desc']}<br>"
        f"<b>Water Quality Class:</b> {point['quality']}<br>"
        f"<b>Water Consumption:</b> {point['consumption']}<br>"
        f"<b>Water Level:</b> {point['level']}"
    )
    
    folium.Marker(
        location=[geom.y, geom.x],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# 6. Save the final map
m.save("42.html")