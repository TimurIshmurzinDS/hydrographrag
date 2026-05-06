import pandas as pd
import geopandas as gpd
from scipy import stats
import folium

# Load datasets (assuming they are in CSV format with 'geometry' column)
rains_data = pd.read_csv('rains.csv')
river_water_levels_data = pd.read_csv('river_water_levels.csv')

# Ensure both datasets have the same geometry column
rains_gdf = gpd.GeoDataFrame(rains_data, geometry=gpd.points_from_xy(rains_data.longitude, rains_data.latitude))
river_water_levels_gdf = gpd.GeoDataFrame(river_water_levels_data, geometry=gpd.points_from_xy(river_water_levels_data.longitude, river_water_levels_data.latitude))

# Interpolate rainfall and water level surfaces
rains_surface = rains_gdf.interpolate(method='linear')
river_water_levels_surface = river_water_levels_gdf.interpolate(method='linear')

# Calculate correlation coefficient between historical rains and river water levels
corr_coef = stats.pearsonr(rains_data['rainfall'], river_water_levels_data['water_level'])[0]

# Create a map centered on the average location of both datasets
avg_lon, avg_lat = (rains_data['longitude'].mean() + river_water_levels_data['longitude'].mean()) / 2, \
                   (rains_data['latitude'].mean() + river_water_levels_data['latitude'].mean()) / 2

m = folium.Map(location=[avg_lat, avg_lon], zoom_start=8)

# Add rainfall data to the map
for idx, row in rains_gdf.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x],
                        radius=5,
                        color='blue',
                        fill=True,
                        fill_opacity=0.5,
                        popup=f'Rainfall: {row["rainfall"]} mm').add_to(m)

# Add river water levels data to the map
for idx, row in river_water_levels_gdf.iterrows():
    folium.CircleMarker(location=[row.geometry.y, row.geometry.x],
                        radius=5,
                        color='red',
                        fill=True,
                        fill_opacity=0.5,
                        popup=f'Water Level: {row["water_level"]} m').add_to(m)

# Save the map
m.save("60.html")

print(f"Correlation coefficient between historical rains and river water levels: {corr_coef}")