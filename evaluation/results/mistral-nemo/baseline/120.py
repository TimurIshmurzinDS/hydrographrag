import folium
import pandas as pd

# Load river water volume data (assuming it's in a CSV file with columns: 'River', 'Date', 'Volume')
river_data = pd.read_csv('river_water_volume.csv')

# Load agricultural water demand data (assuming it's in a CSV file with columns: 'Region', 'Date', 'Demand')
agri_demand_data = pd.read_csv('agri_water_demand.csv')

# Merge both datasets on 'Date' column
merged_data = pd.merge(river_data, agri_demand_data, on='Date')

# Calculate the total water volume from Kurty River and Lepsy River
total_volume = merged_data[(merged_data['River'] == 'Kurty River') | (merged_data['River'] == 'Lepsy River')]['Volume'].sum()

# Calculate the total agricultural water demand
total_demand = merged_data['Demand'].sum()

# Check if the volume is sufficient for agricultural demand
if total_volume >= total_demand:
    print("Объемы воды из рек Kurty River и Lepsy River достаточно для удовлетворения сельскохозяйственного спроса.")
else:
    print("Объемы воды из рек Kurty River и Lespy River не достаточно для удовлетворения сельскохозяйственного спроса.")

# Create a map using folium
m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

# Add rivers to the map (assuming we have longitude and latitude data for rivers)
rivers_data = pd.read_csv('rivers_coordinates.csv')
for _, river in rivers_data.iterrows():
    folium.CircleMarker(location=[river['Latitude'], river['Longitude']], radius=5, color='blue').add_to(m)

# Add agricultural regions to the map (assuming we have longitude and latitude data for agricultural regions)
agri_regions_data = pd.read_csv('agri_regions_coordinates.csv')
for _, region in agri_regions_data.iterrows():
    folium.CircleMarker(location=[region['Latitude'], region['Longitude']], radius=5, color='green').add_to(m)

# Save the map as HTML file
m.save("120.html")