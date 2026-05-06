import pandas as pd
import numpy as np
import folium

# Step 1: Prepare data
data_kurty = pd.read_csv('kurty_river_data.csv')
data_urzhar = pd.read_csv('urzhar_river_data.csv')

# Step 2: Analyze changes in water level
def analyze_water_level(data):
    # Calculate mean and standard deviation of water level
    mean_wl = data['water_level'].mean()
    std_wl = data['water_level'].std()

    # Define threshold values for ecological stress
    lower_threshold = mean_wl - 2 * std_wl
    upper_threshold = mean_wl + 2 * std_wl

    # Identify ecological stress periods based on threshold values
    ecological_stress_kurty = data[(data['water_level'] < lower_threshold) | (data['water_level'] > upper_threshold)]

    return ecological_stress_kurty

ecological_stress_kurty = analyze_water_level(data_kurty)
ecological_stress_urzhar = analyze_water_level(data_urzhar)

# Step 3: Visualize results on a map
m = folium.Map(location=[50.74, 68.12], zoom_start=8) # Set the initial location and zoom level

# Add Kurty River data to the map
folium.CircleMarker(
    location=[data_kurty['latitude'].mean(), data_kurty['longitude'].mean()],
    radius=data_kurty['water_level'].mean(),
    color='blue',
    fill=True,
    fill_opacity=0.5,
    popup=f'Kurty River\nWater Level: {data_kurty["water_level"].mean()}'
).add_to(m)

# Add Urzhar River data to the map
folium.CircleMarker(
    location=[data_urzhar['latitude'].mean(), data_urzhar['longitude'].mean()],
    radius=data_urzhar['water_level'].mean(),
    color='blue',
    fill=True,
    fill_opacity=0.5,
    popup=f'Urzhar River\nWater Level: {data_urzhar["water_level"].mean()}'
).add_to(m)

# Save the map
m.save("108.html")