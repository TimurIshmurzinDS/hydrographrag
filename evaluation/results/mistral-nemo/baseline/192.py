import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# Step 1: Collect data
flow_data = pd.read_csv('river_flow_data.csv')
agro_data = pd.read_csv('agro_data.csv')

# Step 2: Analyze seasonal flow variations
flow_data['month'] = pd.DatetimeIndex(flow_data['date']).month
seasonal_flow = flow_data.groupby('month')['flow'].mean()

# Step 3: Define agroczone vulnerability
agro_data['vulnerability'] = pd.cut(agro_data['vulnerability_score'], bins=[0, 25, 50, 75, 100], labels=['Low', 'Medium', 'High', 'Very High'])

# Step 4: Match flow variations with agroczone vulnerability
merged_data = pd.merge(flow_data, agro_data, left_on='geometry', right_on='geometry')
risk_scores = merged_data.groupby(['month', 'vulnerability'])['flow'].mean()

# Step 5: Visualize results on a map
m = folium.Map(location=[43.2389, 76.8897], zoom_start=10)

for index, row in risk_scores.iterrows():
    month, vulnerability, flow = index
    geometry = Point(row['geometry'].x, row['geometry'].y)
    popup_text = f'Month: {month}, Vulnerability: {vulnerability}, Flow: {flow}'
    folium.Marker(geometry, popup=popup_text).add_to(m)

# Save the map as an HTML file
m.save("192.html")