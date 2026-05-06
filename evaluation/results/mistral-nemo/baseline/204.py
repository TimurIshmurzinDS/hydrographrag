import pandas as pd
import numpy as np
import folium

# Load historical flow data for Byzhy River and Urzhar River
byzhy_data = pd.read_csv('byzhy_flow.csv')
urzhar_data = pd.read_csv('urzhar_flow.csv')

# Calculate mean annual flow (MAF) for each river
byzhy_maf = byzhy_data['flow'].mean()
urzhar_maf = urzhar_data['flow'].mean()

# Create hydrological curve for each river
byzhy_hydro_curve = byzhy_data.groupby(byzhy_data['month'])['flow'].apply(lambda x: (x / byzhy_maf) * 100).reset_index()
urzhar_hydro_curve = urzhar_data.groupby(urzhar_data['month'])['flow'].apply(lambda x: (x / urzhar_maf) * 100).reset_index()

# Create a map centered between the two rivers
m = folium.Map(location=[(byzhy_data['lat'].mean() + urzhar_data['lat'].mean())/2, (byzhy_data['lon'].mean() + urzhar_data['lon'].mean())/2], zoom_start=8)

# Add data points to the map for each river
for idx, row in byzhy_hydro_curve.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color='blue').add_to(m)
folium.PolyLine(locations=list(zip(byzhy_data['lon'], byzhy_data['lat']))).add_to(m)

for idx, row in urzhar_hydro_curve.iterrows():
    folium.CircleMarker(location=[row['lat'], row['lon']], radius=5, color='red').add_to(m)
folium.PolyLine(locations=list(zip(urzhar_data['lon'], urzhar_data['lat']))).add_to(m)

# Save the map as HTML file
m.save("204.html")