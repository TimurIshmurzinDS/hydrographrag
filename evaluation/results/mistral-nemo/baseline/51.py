import pandas as pd
import folium

# Step 1: Prepare data
data = pd.read_csv('kurty_river_water_levels.csv')  # Assume the data is in a CSV file with columns 'Date' and 'WaterLevel'

# Convert date column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Step 2: Filter data for summer and winter months
summer_data = data[(data['Date'].dt.month >= 6) & (data['Date'].dt.month <= 8)]
winter_data = data[(data['Date'].dt.month >= 12) & (data['Date'].dt.month <= 2)]

# Step 3: Calculate average water levels
avg_summer_water_level = summer_data['WaterLevel'].mean()
avg_winter_water_level = winter_data['WaterLevel'].mean()

# Step 4: Visualize on map using folium
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13)  # Starting location is Kurty River's approximate coordinates

folium.Marker([51.5074, -0.1278], popup=f'Средний расход воды летом: {avg_summer_water_level:.2f}\nСредний расход воды зимой: {avg_winter_water_level:.2f}').add_to(m)

# Save the map as '51.html'
m.save("51.html")