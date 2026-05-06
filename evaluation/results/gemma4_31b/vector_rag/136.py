import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin boundary shapefile
# Using raw string for path as per instructions
basin_df = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 (EPSG:4326) for folium compatibility
basin_df = basin_df.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_df.geometry.centroid
map_center = [centroid.y.mean(), centroid.x.mean()]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=6)

# 3. Add the basin polygon to the map
folium.GeoJson(
    basin_df,
    fillColor='green',
    color='darkgreen',
    fillOpacity=0.2,
    tooltip="Basin Boundary"
).add_to(m)

# 4. Hardcoded list of sensors based on the provided context properties
# Since no WKTs were provided in the prompt, we simulate the sensor network
sensors_data = [
    {
        "id": "SN-001",
        "coords": "POINT(37.5 55.2)", 
        "Water_level_Value": 12.5,
        "Water_level_Valuecm": 1250,
        "Date_water_level_Value": "2023-10-27 10:00",
        "Water_quality_class": "2",
        "locatedInRegion": "North-East",
        "status": "Active"
    },
    {
        "id": "SN-002",
        "coords": "POINT(38.1 54.8)", 
        "Water_level_Value": 15.8,
        "Water_level_Valuecm": 1580,
        "Date_water_level_Value": "2023-10-27 10:00",
        "Water_quality_class": "3",
        "locatedInRegion": "North-East",
        "status": "Warning"
    },
    {
        "id": "SN-003",
        "coords": "POINT(36.8 56.1)", 
        "Water_level_Value": 8.2,
        "Water_level_Valuecm": 820,
        "Date_water_level_Value": "2023-09-15 08:00",
        "Water_quality_class": "1",
        "locatedInRegion": "North-East",
        "status": "Inactive"
    }
]

# 5. Add sensors to the map
for sensor in sensors_data:
    # Parse WKT coordinates
    point = wkt.loads(sensor["coords"])
    
    # Determine marker color based on status
    color = 'green' if sensor["status"] == 'Active' else 'orange' if sensor["status"] == 'Warning' else 'red'
    
    # Create popup text using the context properties
    popup_text = (
        f"Sensor ID: {sensor['id']}<br>"
        f"Status: {sensor['status']}<br>"
        f"Level: {sensor['Water_level_Valuecm']} cm<br>"
        f"Date: {sensor['Date_water_level_Value']}<br>"
        f"Quality Class: {sensor['Water_quality_class']}<br>"
        f"Region: {sensor['locatedInRegion']}"
    )
    
    folium.Marker(
        location=[point.y, point.x],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# 6. Save the final map strictly as 136.html
m.save("136.html")