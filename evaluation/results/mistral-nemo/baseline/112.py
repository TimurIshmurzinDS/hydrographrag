import folium

# Data about water consumption levels for each river
kurty_river_water_consumption = 50
urzhar_river_water_consumption = 70
byzhy_river_water_consumption = 60

# Create a map centered around the average location of the rivers
m = folium.Map(location=[53.9, 62.8], zoom_start=4)

# Define colors for water consumption levels
colors = ['green', 'yellow', 'red']

# Add rivers to the map with their respective water consumption levels
for river, consumption in zip(['Kurty River', 'Urzhar River', 'Byzhy River'], [kurty_river_water_consumption, urzhar_river_water_consumption, byzhy_river_water_consumption]):
    folium.CircleMarker(location=[53.9, 62.8], color=colors[consumption//10], fill=True).add_to(m)
    folium.Popup(river + ': ' + str(consumption) + '%', parse_html=True).add_to(m)

# Save the map to an HTML file
m.save("112.html")