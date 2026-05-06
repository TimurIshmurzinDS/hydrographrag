import folium

# Example data from Kishi Almaty River sensors (replace with actual sensor data)
temperature = [25, 26, 27, 28, 29]
humidity = [30, 35, 40, 45, 50]
sunlight_intensity = [1000, 1200, 1400, 1600, 1800]

# Calculate average values
avg_temperature = sum(temperature) / len(temperature)
avg_humidity = sum(humidity) / len(humidity)
avg_sunlight_intensity = sum(sunlight_intensity) / len(sunlight_intensity)

print("Average Temperature:", avg_temperature)
print("Average Humidity:", avg_humidity)
print("Average Sunlight Intensity:", avg_sunlight_intensity)

# Create a map centered on Almaty (replace with actual coordinates)
m = folium.Map(location=[43.25, 76.92], zoom_start=10)

# Add markers for sensor locations (replace with actual sensor coordinates)
folium.Marker([43.25, 76.92], popup="Kishi Almaty River Sensor").add_to(m)

# Save the map
m.save("217.html")