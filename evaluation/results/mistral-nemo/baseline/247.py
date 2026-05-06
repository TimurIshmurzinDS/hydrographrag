import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import folium

# Load data about river tributaries and bitcoin mining pools
tributaries = gpd.read_file("tributaries.shp")
mining_pools = pd.read_csv("mining_pools.csv")

# Calculate distance from each tributary to the nearest mining pool
geometry = [Point(xy) for xy in zip(mining_pools['longitude'], mining_pools['latitude'])]
gdf_mining_pools = gpd.GeoDataFrame(mining_pools, geometry=geometry)
distances = gpd.sjoin_nearest(tributaries, gdf_mining_pools, how="left")

# Calculate time for data transmission between each tributary and its nearest mining pool
transmission_time = distances['distance'] / 1000 * 24 * 60 * 60 / (distances['bandwidth'] * 8)

# Calculate costs for electricity and other operational expenses
electricity_costs = tributaries['power'] * tributaries['tariff']
cooling_costs = tributaries['power'] * tributaries['cooling_factor']
transportation_costs = tributaries['distance'] * tributaries['transportation_cost']

total_costs = electricity_costs + cooling_costs + transportation_costs

# Optimize locations for bitcoin mining
optimized_locations = total_costs.min()

# Create a map using Folium library
m = folium.Map(location=[tributaries['latitude'].mean(), tributaries['longitude'].mean()], zoom_start=8)

for idx, row in tributaries.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

for idx, row in gdf_mining_pools.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=3,
        color='red',
        fill=True,
        fill_opacity=0.6
    ).add_to(m)

m.save("247.html")