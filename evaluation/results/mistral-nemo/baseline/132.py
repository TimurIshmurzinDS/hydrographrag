import pandas as pd
import folium

# Load data for Lepsy River and Tekes River
lepsy_data = pd.read_csv('lepsy_river.csv')
tekes_data = pd.read_csv('tekes_river.csv')

# Find the year with maximum discharge for each river
max_lepsy_year = lepsy_data['year'][lepsy_data['discharge'].idxmax()]
max_tekes_year = tekes_data['year'][tekes_data['discharge'].idxmax()]

# Print results
print(f"Год с самым высоким уровнем стока в реке Лепси: {max_lepsy_year}")
print(f"Год с самым высоким уровнем стока в реке Текес: {max_tekes_year}")

# If visualization is required, create a map using folium
m = folium.Map(location=[50.7469, 86.2583], zoom_start=10)  # Starting location and zoom level can be adjusted

# Add Lepsy River with its year of maximum discharge
folium.Marker([lepsy_data['latitude'].iloc[0], lepsy_data['longitude'].iloc[0]], popup=f"Лепси река\nГод с наибольшим стоком: {max_lepsy_year}").add_to(m)

# Add Tekes River with its year of maximum discharge
folium.Marker([tekes_data['latitude'].iloc[0], tekes_data['longitude'].iloc[0]], popup=f"Текес река\nГод с наибольшим стоком: {max_tekes_year}").add_to(m)

# Save the map as '132.html'
m.save("132.html")