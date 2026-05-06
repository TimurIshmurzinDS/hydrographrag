import pandas as pd
import folium

# Step 1: Collect data
tekeli_data = pd.read_csv('tekeli_river_water_level.csv')
lepsy_data = pd.read_csv('lepsy_river_water_level.csv')

# Step 2: Analyze data
 tekeli_avg = tekeli_data['water_level'].mean()
 lepsy_avg = lespy_data['water_level'].mean()

 tekeli_std_dev = tekeli_data['water_level'].std()
 lepsy_std_dev = lepsy_data['water_level'].std()

# Step 3: Evaluate agricultural sustainability
# Assuming that the minimum water level required for agriculture is 5 meters
if tekeli_avg < 5 or lepsy_avg < 5:
    print("Agricultural sustainability may be at risk due to low average water levels.")

if tekeli_std_dev > 2 or lepsy_std_dev > 2:
    print("Agricultural sustainability may be at risk due to high variability in water levels.")

# Step 4: Visualize results
m = folium.Map(location=[51.5074, -0.1278], zoom_start=6)

folium.Marker([tekeli_data['latitude'].mean(), tekeli_data['longitude'].mean()],
              popup='Tekeli River\nAverage water level: {:.2f} meters\nStandard deviation: {:.2f}'.format(tekeli_avg, tekeli_std_dev)).add_to(m)

folium.Marker([lepsy_data['latitude'].mean(), lepsy_data['longitude'].mean()],
              popup='Lepsy River\nAverage water level: {:.2f} meters\nStandard deviation: {:.2f}'.format(lepsy_avg, lepsy_std_dev)).add_to(m)

m.save("116.html")