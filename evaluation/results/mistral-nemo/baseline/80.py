import requests
import folium

# Step 1: Get data about water flow on Tokyraun and Koktal rivers
def get_water_flow_data(river_name):
    # Replace this function with actual API call or data import
    return {"flow_rate": 50, "basin_area": 200}

tokyraun_data = get_water_flow_data("Tokyraun")
koktal_data = get_water_flow_data("Koktal")

# Step 2: Normalize the data
def normalize_data(data):
    return data["flow_rate"] / data["basin_area"]

normalized_tokyraun_data = normalize_data(tokyraun_data)
normalized_koktal_data = normalize_data(koktal_data)

# Step 3: Create a map using folium
m = folium.Map(location=[50, 70], zoom_start=6)  # Replace with actual coordinates

def add_river_to_map(river_name, normalized_flow_rate):
    # Assume we have coordinates for the rivers
    if river_name == "Tokyraun":
        coords = [(49.83, 72.51), (50.21, 72.67)]
    elif river_name == "Koktal":
        coords = [(50.54, 73.12), (50.87, 73.39)]

    folium.PolyLine(coords, weight=normalized_flow_rate*10, color='blue').add_to(m)

add_river_to_map("Tokyraun", normalized_tokyraun_data)
add_river_to_map("Koktal", normalized_koktal_data)

# Step 4: Save the map
m.save("80.html")