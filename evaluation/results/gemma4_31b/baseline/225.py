import folium
import numpy as np
from folium.plugins import AntPath

def create_black_hole_simulation():
    # 1. Coordinates for Kishi Almaty River (Approximate path from mountains to city)
    # Format: [lat, lon]
    river_coords = [
        [43.2350, 77.0100], [43.2200, 77.0200], [43.2100, 77.0350], 
        [43.2000, 77.0500], [43.1900, 77.0700], [43.1800, 77.0900],
        [43.1700, 77.1100], [43.1600, 77.1300]
    ]
    
    # 2. Define the Singularity Point (The "Black Hole" center)
    # Placing it roughly in the middle of the river path
    singularity = [43.2000, 77.0500]
    
    # Initialize the map centered around the singularity
    m = folium.Map(location=singularity, zoom_start=13, tiles='CartoDB dark_matter')
    
    # 3. Draw the original river path using AntPath for "flow" effect
    AntPath(river_coords, weight=5, color='blue', delay=100, dash_array=[10, 20]).add_to(m)
    
    # 4. Simulate the "Gravitational Pull"
    # We create a set of points along the river and draw lines towards the singularity
    for point in river_coords:
        # Calculate distance (simplified Euclidean for visualization)
        dist = np.sqrt((point[0] - singularity[0])**2 + (point[1] - singularity[1])**2)
        
        # Create a "pull" line from the river point to the black hole
        # Color changes from blue (water) to purple/black (event horizon)
        color = 'blue' if dist > 0.03 else 'purple'
        
        folium.PolyLine(
            locations=[point, singularity],
            weight=2,
            color=color,
            opacity=0.6,
            line_dash_pattern='5, 10'
        ).add_to(m)

    # 5. Create the "Black Hole" visual marker
    # A large black circle representing the Event Horizon
    folium.Circle(
        location=singularity,
        radius=500, # 500 meters
        color='black',
        fill=True,
        fill_color='black',
        fill_opacity=0.9,
        popup="SINGULARITY: Kishi Almaty Black Hole"
    ).add_to(m)
    
    # Add a central point for the singularity
    folium.CircleMarker(
        location=singularity,
        radius=5,
        color='white',
        fill=True,
        fill_color='white'
    ).add_to(m)

    # Save the map
    m.save("225.html")
    print("Simulation complete. Map saved as 225.html")

if __name__ == "__main__":
    create_black_hole_simulation()