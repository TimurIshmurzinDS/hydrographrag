import requests
import folium

# Step 1: Load water level data for all posts on Prokhodnaya River
def get_water_level_data():
    # Replace this function with actual API call or file loading logic
    return {
        "post1": {"id": 1, "latitude": 55.7558, "longitude": 37.6173, "last_level": 2.5},
        "post2": {"id": 2, "latitude": 55.7490, "longitude": 37.6217, "last_level": 2.8},
        # Add more posts as needed
    }

# Step 2: Filter data to get latest water levels for each post
def filter_latest_water_levels(data):
    return {post_id: data[post_id]["last_level"] for post_id in sorted(data.keys())}

# Step 3: Create a dictionary with post IDs as keys and latest water levels as values
water_level_data = get_water_level_data()
latest_water_levels = filter_latest_water_levels(water_level_data)

# Step 4: Load geodata for each post on Prokhodnaya River (if needed)
def get_geodata(post_id):
    # Replace this function with actual geodata loading logic
    return {
        "post1": {"latitude": 55.7558, "longitude": 37.6173},
        "post2": {"latitude": 55.7490, "longitude": 37.6217},
        # Add more posts as needed
    }

# Step 5: Create a map with folium and add all posts as markers
m = folium.Map(location=[55.7558, 37.6173], zoom_start=14)

geodata = get_geodata()
for post_id, level in latest_water_levels.items():
    lat, lon = geodata[post_id]["latitude"], geodata[post_id]["longitude"]
    folium.Marker([lat, lon], popup=f"Уровень воды: {level} м").add_to(m)

# Step 6: Display last recorded water levels on the map
for post_id in latest_water_levels.keys():
    lat, lon = geodata[post_id]["latitude"], geodata[post_id]["longitude"]
    folium.CircleMarker(
        location=[lat, lon],
        radius=5,
        color="blue",
        fill=True,
        fill_color="blue",
        popup=f"Уровень воды: {latest_water_levels[post_id]} м",
    ).add_to(m)

# Step 7: Save the map as "67.html"
m.save("67.html")