import folium

# Assuming you have data on the anomaly and its location

# Create a map centered on the Karatal River
m = folium.Map(location=[42.8750, 76.3167], zoom_start=10)

# Add a marker to highlight the location of the anomaly
folium.Marker(location=[42.8750, 76.3167], popup="Karatal River Anomaly").add_to(m)

# Save the map
m.save("222.html")

print("Recommendation: Due to the anomaly detected in Karatal River, it is advisable to use alternative water sources or apply purification methods before using the water for cooking.")