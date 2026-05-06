import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load hydropost data and coordinates
hydroposts = pd.read_csv('hydroposts.csv')
geometry = [Point(xy) for xy in zip(hydroposts['longitude'], hydroposts['latitude'])]
gdf_hydroposts = gpd.GeoDataFrame(hydroposts, geometry=geometry)

# Load water flow data
water_flow = pd.read_csv('water_flow.csv')

# Merge hydropost and water flow data
merged_data = pd.merge(gdf_hydroposts, water_flow, on='hydropost_id')

# Calculate average water flow for each hydropost in previous years
avg_water_flow = merged_data.groupby('hydropost_id')['water_flow'].transform(lambda x: x.expanding().mean())

# Define threshold for significant increase (e.g., 50% above average)
threshold = 1.5

# Find hydroposts with significant water flow increase
increased_water_flow = merged_data[merged_data['water_flow'] > avg_water_flow * threshold]

# Create a map using folium
m = folium.Map(location=[hydroposts['latitude'].mean(), hydroposts['longitude'].mean()], zoom_start=8)

# Add increased water flow hydroposts to the map as markers with popups showing their IDs and water flow values
for index, row in increased_water_flow.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Hydropost ID: {row["hydropost_id"]}, Water Flow: {row["water_flow"]}').add_to(m)

# Save the map as HTML file
m.save("84.html")