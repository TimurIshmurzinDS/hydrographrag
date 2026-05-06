import folium
import numpy as np
import pandas as pd
import random

def simulate_satellite_launch():
    # 1. Coordinates for the Ili River (approximate path from China to Lake Balkhash)
    ili_river_coords = [
        [43.2, 80.1], [43.5, 81.2], [43.8, 82.5], 
        [43.7, 83.8], [43.5, 85.0], [43.2, 86.1], [43.0, 87.5]
    ]
    
    # Launch site coordinates (near the river basin)
    launch_site = [43.5, 84.0]
    # Target orbit projection point
    orbit_point = [46.0, 88.0]

    # 2. Simulate Water Discharge Data (m3/s)
    # Let's simulate 30 days of discharge data
    days = 30
    discharge_values = [random.uniform(100, 500) for _ in range(days)]
    df_discharge = pd.DataFrame({'day': range(1, days+1), 'flow': discharge_values})
    
    # Calculate total volume in cubic meters (flow * seconds in a day)
    seconds_in_day = 24 * 3600
    total_volume = df_discharge['flow'].sum() * seconds_in_day
    
    # 3. Conversion Logic
    # Threshold: 1.5 trillion cubic meters to "power" the launch
    threshold_volume = 1.5e12 
    is_launched = total_volume >= threshold_volume
    
    print(f"Total Water Volume accumulated: {total_volume:.2e} m3")
    print(f"Threshold for launch: {threshold_volume:.2e} m3")
    print(f"Launch Status: {'SUCCESS' if is_launched else 'FAILED - Insufficient Water Energy'}")

    # 4. GIS Visualization
    # Initialize map centered on the Ili River region
    m = folium.Map(location=[43.5, 84.0], zoom_start=6, tiles='CartoDB positron')

    # Draw the Ili River
    folium.PolyLine(ili_river_coords, color='blue', weight=4, opacity=0.8, 
                    tooltip="Ili River (Water Energy Source)").add_to(m)

    # Mark the Monitoring Station
    folium.CircleMarker(location=[43.7, 82.5], radius=6, color='red', fill=True, 
                        popup="Hydrological Station: Measuring Discharge").add_to(m)

    # Mark the Launch Site
    folium.Marker(location=launch_site, icon=folium.Icon(color='green', icon='rocket'), 
                  popup="Satellite Launch Site").add_to(m)

    # If launch is successful, draw the trajectory
    if is_launched:
        folium.PolyLine([launch_site, orbit_point], color='purple', weight=3, 
                        dash_array='10', tooltip="Satellite Trajectory to Orbit").add_to(m)
        
        # Add a marker for the satellite in "orbit"
        folium.Marker(location=orbit_point, icon=folium.Icon(color='darkblue', icon='info-sign'), 
                      popup="Satellite in LEO").add_to(m)
    else:
        # Add a warning marker if not enough water
        folium.Marker(location=launch_site, icon=folium.Icon(color='orange', icon='warning'), 
                      popup="Waiting for more water discharge...").add_to(m)

    # Save the map
    m.save("235.html")
    print("Map has been saved as 235.html")

if __name__ == "__main__":
    simulate_satellite_launch()