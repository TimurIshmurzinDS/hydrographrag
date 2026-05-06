import folium

def calculate_alpha_centauri_distance():
    # --- Constants ---
    # Distance to Alpha Centauri in light years
    dist_ly = 4.37 
    # 1 light year in meters
    ly_to_meters = 9.461e15 
    # Average width of the Karaoy river in meters (estimated value)
    karaoy_width_m = 20.0 
    
    # --- Calculations ---
    # Total distance in meters
    total_distance_m = dist_ly * ly_to_meters
    
    # Distance in terms of "Karaoy River Widths"
    distance_in_widths = total_distance_m / karaoy_width_m
    
    print(f"Total distance to Alpha Centauri: {total_distance_m:.2e} meters")
    print(f"Average width of Karaoy River: {karaoy_width_m} meters")
    print(f"Distance in 'Karaoy Widths': {distance_in_widths:.2e} units")
    
    return distance_in_widths

def create_map():
    # Approximate coordinates for the Karaoy river region (Example: Northern Russia/Siberia)
    # Note: Coordinates are illustrative for the GIS task
    lat, lon = 65.5, 70.0 
    
    # Initialize folium map
    m = folium.Map(location=[lat, lon], zoom_start=6, control_scale=True)
    
    # Add a marker for the reference point (Karaoy River)
    folium.Marker(
        [lat, lon], 
        popup="Reference Point: Karaoy River Width", 
        tooltip="Start of Measurement"
    ).add_to(m)
    
    # Add a caption to the map
    folium.map.Marker([lat, lon], 
                      icon=folium.Icon(color='blue', icon='info-sign')).add_to(m)
    
    # Save the map strictly as 253.html
    m.save("253.html")
    print("Map has been saved as 253.html")

if __name__ == "__main__":
    # Execute the modeling calculation
    result = calculate_alpha_centauri_distance()
    
    # Execute the GIS visualization
    create_map()