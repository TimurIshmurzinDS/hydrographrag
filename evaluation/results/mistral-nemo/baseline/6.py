import folium

# Step 1: Load sensor data (Assuming we have a function `load_sensor_data` that returns the status)
def load_sensor_data(river_name):
    # Replace this with actual implementation to fetch data from your source
    if river_name == "Kumbel River":
        return "Active"
    else:
        return "Inactive"

# Step 2: Determine sensor status
river_name = "Kumbel River"
sensor_status = load_sensor_data(river_name)

# Step 3: Visualize on map using Folium
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13)  # Starting location (London), adjust as needed

if sensor_status == "Active":
    color = "green"
else:
    color = "red"

folium.CircleMarker(
    location=[51.5074, -0.1278],
    radius=6,
    color=color,
    fill=True,
    fill_color=color
).add_to(m)

# Save the map as HTML file
m.save("6.html")