import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Load data (Assuming it's a CSV file with columns: 'River', 'Location', 'FlowRate')
data = pd.read_csv('river_data.csv')

# Filter data for Koktal River and Baskan River
koktal_data = data[data['River'] == 'Koktal River']
baskan_data = data[data['River'] == 'Baskan River']

# Convert data to GeoDataFrame
geometry = [Point(xy) for xy in zip(koktal_data['Longitude'], koktal_data['Latitude'])]
gdf_koktal = gpd.GeoDataFrame(koktal_data, geometry=geometry)
gdf_baskan = gpd.GeoDataFrame(baskan_data, geometry=geometry)

# Perform geospatial analysis and modeling (This is a simplified example. You might need to use more advanced methods)
risk_score_koktal = gdf_koktal['FlowRate'].rank(pct=True) * 100
risk_score_baskan = gdf_baskan['FlowRate'].rank(pct=True) * 100

# Add risk score to GeoDataFrame
gdf_koktal['RiskScore'] = risk_score_koktal
gdf_baskan['RiskScore'] = risk_score_baskan

# Create a map using Folium
m = folium.Map(location=[43.2, 68.9], zoom_start=8)  # Starting location and zoom level

# Add Koktal River data to the map
for _, row in gdf_koktal.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5,
        popup=f'Risk Score: {row.RiskScore:.2f}%'
    ).add_to(m)

# Add Baskan River data to the map
for _, row in gdf_baskan.iterrows():
    folium.CircleMarker(
        location=(row.geometry.y, row.geometry.x),
        radius=5,
        color='red',
        fill=True,
        fill_opacity=0.5,
        popup=f'Risk Score: {row.RiskScore:.2f}%'
    ).add_to(m)

# Save the map
m.save("85.html")