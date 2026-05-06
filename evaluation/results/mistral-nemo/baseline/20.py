import folium
import geopandas as gpd
from shapely.geometry import Point

# Load data (Assuming you have a CSV file with columns: 'latitude', 'longitude', 'water_height', 'river_width')
data = gpd.read_file('batareyka_river_data.csv')

# Constants
g = 9.81  # ускорение свободного падения (м/с^2)
L = 5000  # длина реки Batareyka River (м)

# Calculate cross-sectional area of the river
data['cross_section_area'] = data['water_height'] * data['river_width']

# Calculate average flow speed
data['flow_speed'] = ((2 * g * data['water_height']) ** 0.5)

# Calculate friction coefficient
data['friction_coefficient'] = (data['water_height'] / L) ** (1/6)

# Calculate discharge with friction coefficient
data['discharge'] = data['cross_section_area'] * data['flow_speed'] / data['friction_coefficient']

# Create a map centered on Batareyka River
m = folium.Map(location=[53.9, 27.5], zoom_start=10)

# Add river geometry to the map (Assuming you have a GeoJSON file for Batareyka River)
river_geometry = gpd.read_file('batareyka_river_geometry.geojson')
folium.GeoJson(river_geometry, style_function=lambda x: {'fillColor': 'blue', 'color': 'black'}).add_to(m)

# Add data points to the map with discharge values as popups
for _, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Discharge: {row["discharge"]:.2f} m³/s').add_to(m)

# Save the final map
m.save("batareyka_river_discharge.html")