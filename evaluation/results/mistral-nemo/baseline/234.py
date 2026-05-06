import geopandas as gpd
import pandas as pd
import numpy as np
import folium

# Load datasets
pizza_data = pd.read_csv('pizza_recipes.csv')
flood_data = gpd.read_file('sharyn_floods.shp')

# Preprocess pizza recipe data
pizza_data['ingredients'] = pizza_data['recipe'].str.extract(r'(\w+ \d+)', expand=True)
pizza_data[['ingredient', 'quantity']] = pizza_data['ingredients'].str.split(' ', 1).str.map(pd.Series)

# Preprocess flood data to get seasonal flood zones
seasonal_floods = flood_data[flood_data['season'] == 'spring']  # Assuming spring is the season of interest

# Calculate distance from preparation locations to flooded areas
def calculate_distance(row, gdf):
    return row.distance(gdf.iloc[gdf.geometry.distance(row.geometry).idxmin()])

pizza_data['distance_to_flood'] = pizza_data.apply(calculate_distance, args=(seasonal_floods,), axis=1)

# Determine safe preparation locations based on safety criteria (e.g., distance > 500m)
safe_distance_threshold = 500
pizza_data['is_safe'] = pizza_data['distance_to_flood'] > safe_distance_threshold

# Create an interactive map using folium
m = folium.Map(location=[53.2457, 69.9718], zoom_start=8)  # Approximate coordinates for River Sharyn

# Add flood zones to the map
folium.GeoJson(seasonal_floods[['geometry']].to_json(), style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)

# Add preparation locations to the map (safe and unsafe)
for index, row in pizza_data.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']],
                        radius=5,
                        color='green' if row['is_safe'] else 'red',
                        fill=True).add_to(m)

# Save the final map
m.save("234.html")