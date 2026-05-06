import folium

# Step 1: Collect data
average_flow_rate = 50 # m3/s (example value)
irrigation_areas = {
    'area1': 1000, # hectares
    'area2': 800,
    ...
}
water_needs_per_hectare = {
    'area1': 5000, # m3/ha (example value)
    'area2': 4500,
    ...
}

# Step 2: Calculate water demand
total_water_demand = sum([irrigation_areas[area] * water_needs_per_hectare[area] for area in irrigation_areas])

# Step 3: Calculate water deficit
water_deficit = total_water_demand - average_flow_rate

# Visualization on a map (example location of Ayagoz River)
m = folium.Map(location=[45.015, 68.729], zoom_start=10)

folium.Marker([45.015, 68.729], popup='Water Deficit: {} m3/s'.format(water_deficit)).add_to(m)

# Save the final map
m.save("35.html")