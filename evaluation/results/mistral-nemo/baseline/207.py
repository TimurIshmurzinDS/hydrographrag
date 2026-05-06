import pandas as pd
import numpy as np
import folium

# Load data for Emel River and Turgen River water levels
emel_data = pd.read_csv('emel_river_water_levels.csv')
turgen_data = pd.read_csv('turgen_river_water_levels.csv')

# Calculate mean water level for each year in the last two decades
emel_mean = emel_data.groupby(pd.Grouper(freq='Y')).mean()['water_level']
turgen_mean = turgen_data.groupby(pd.Grouper(freq='Y')).mean()['water_level']

# Define threshold values for extreme events (e.g., Q1 and Q3)
Q1_emel, Q3_emel = emel_data['water_level'].quantile([0.25, 0.75])
Q1_turgen, Q3_turgen = turgen_data['water_level'].quantile([0.25, 0.75])

# Filter data for extreme events
emel_extreme = emel_data[(emel_data['water_level'] > Q3_emel) | (emel_data['water_level'] < Q1_emel)]
turgen_extreme = turgen_data[(turgen_data['water_level'] > Q3_turgen) | (turgen_data['water_level'] < Q1_turgen)]

# Calculate frequency of extreme events
emel_freq = len(emel_extreme) / len(emel_data)
turgen_freq = len(turgen_extreme) / len(turgen_data)

# Create a map centered between Emel River and Turgen River
m = folium.Map(location=[(emel_data['latitude'].mean() + turgen_data['latitude'].mean())/2, (emel_data['longitude'].mean() + turgen_data['longitude'].mean())/2], zoom_start=8)

# Add markers for Emel River and Turgen River with their extreme event frequencies
folium.Marker([emel_data['latitude'].mean(), emel_data['longitude'].mean()], popup=f'Emel River\nFrequency of Extreme Events: {emel_freq:.4f}').add_to(m)
folium.Marker([turgen_data['latitude'].mean(), turgen_data['longitude'].mean()], popup=f'Turgen River\nFrequency of Extreme Events: {turgen_freq:.4f}').add_to(m)

# Save the map as "207.html"
m.save("207.html")