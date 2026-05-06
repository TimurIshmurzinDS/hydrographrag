import folium
import numpy as np
from shapely.geometry import LineString, Polygon

def solve_pasta_flood_problem():
    # 1. Coordinates for the Koktal River area (Approximate simulation)
    # Koktal river is located in Kazakhstan
    river_coords = [
        (52.10, 78.50), 
        (52.12, 78.55), 
        (52.15, 78.58), 
        (52.18, 78.62), 
        (52.22, 78.65), 
        (52.25, 78.70)
    ]
    
    # Create a LineString for the river
    river_line = LineString(river_coords)
    
    # 2. Simulate Spring Flood (Buffer analysis)
    # In a real GIS task, we would use a DEM and water level data.
    # Here, we simulate a flood buffer of ~2km (approx 0.02 degrees)
    flood_buffer_dist = 0.02 
    flood_zone = river_line.buffer(flood_buffer_dist)
    
    # 3. Calculate "Culinary Metrics"
    # Approximate area calculation (simplified for simulation)
    # Area of a buffer around a line is roughly Length * 2 * Width
    length_deg = river_line.length
    area_sq_deg = length_deg * (flood_buffer_dist * 2)
    
    # Convert approximate degrees to km (1 deg ~ 111km)
    area_km2 = area_sq_deg * (111 * 111)
    
    # Logic for the recipe
    pasta_amount_kg = area_km2 * 0.5  # 0.5kg per km2
    boiling_time_min = int(flood_buffer_dist * 1000 / 2) # Width in meters / 2
    
    # Sinuosity check for pasta type
    # (Straight line distance vs actual length)
    straight_dist = LineString([river_coords[0], river_coords[-1]]).length
    sinuosity = length_deg / straight_dist
    pasta_type = "Fettuccine (Curvy)" if sinuosity > 1.1 else "Penne (Straight)"

    # 4. Visualization
    # Center the map
    m = folium.Map(location=[52.15, 78.60], zoom_start=11, tiles='OpenStreetMap')
    
    # Add the river centerline
    folium.PolyLine(river_coords, color="blue", weight=5, opacity=0.8, tooltip="Koktal River").add_to(m)
    
    # Add the flood zone
    # Convert shapely polygon to list of coordinates for folium
    exterior_coords = list(flood_zone.exterior.coords)
    folium.Polygon(
        locations=exterior_coords, 
        color="cyan", 
        fill=True, 
        fill_color="cyan", 
        fill_opacity=0.3, 
        tooltip="Spring Flood Zone"
    ).add_to(m)
    
    # Save the map
    m.save("231.html")
    
    # 5. Final Recipe Output
    print("--- GEOSPATIAL PASTA RECIPE ---")
    print(f"Based on the Koktal River flood data:")
    print(f"1. Pasta Type: {pasta_type}")
    print(f"2. Quantity: {pasta_amount_kg:.2f} kg of pasta")
    print(f"3. Boiling Time: {boiling_time_min} minutes")
    print(f"4. Instructions: Boil water until it reaches the level of the spring flood,")
    print(f"   add the {pasta_type}, and cook for {boiling_time_min} minutes.")
    print("------------------------------")
    print("Map has been saved as 231.html")

if __name__ == "__main__":
    solve_pasta_flood_problem()