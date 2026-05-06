import requests
import folium

def get_river_coordinates(river_names):
    """
    Fetch coordinates for specified rivers from OpenStreetMap via Overpass API.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Constructing the Overpass QL query
    # We search for 'way' elements with the specified names and request their geometry
    names_query = "|".join(river_names)
    query = f'way["name"~"{names_query}"]; out geom;'
    
    response = requests.get(overpass_url, params={'data': query})
    
    if response.status_code != 200:
        print("Error fetching data from Overpass API")
        return {}

    data = response.json()
    rivers_coords = {}

    for element in data.get('elements', []):
        name = element.get('tags', {}).get('name', 'Unknown')
        # Extract geometry coordinates
        geometry = element.get('geometry', [])
        coords = [(point['lat'], point['lon']) for point in geometry]
        
        if name not in rivers_coords:
            rivers_coords[name] = []
        
        # Append coordinates to the specific river
        rivers_coords[name].extend(coords)
        
    return rivers_coords

def main():
    # List of rivers to find
    target_rivers = ["Уржар", "Дос", "Каратал"]
    
    print("Fetching coordinates from OSM...")
    rivers_data = get_river_coordinates(target_rivers)
    
    if not rivers_data:
        print("No data found for the specified rivers.")
        return

    # Print coordinates to console as requested
    for river, coords in rivers_data.items():
        print(f"\nRiver: {river}")
        print(f"Coordinates count: {len(coords)}")
        print(f"First 5 coordinates: {coords[:5]}")

    # Initialize folium map centered around Kazakhstan
    m = folium.Map(location=[46.0, 70.0], zoom_start=5, tiles='CartoDB positron')

    # Colors for different rivers
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    
    for i, (river, coords) in enumerate(rivers_data.items()):
        color = colors[i % len(colors)]
        # Add the river line to the map
        folium.PolyLine(
            locations=coords, 
            color=color, 
            weight=3, 
            opacity=0.8, 
            popup=river
        ).add_to(m)
        
        # Add a marker at the start of the river
        folium.Marker(
            location=coords[0], 
            popup=f"Start of {river}", 
            icon=folium.Icon(color=color)
        ).add_to(m)

    # Save the map strictly as 103.html
    m.save("103.html")
    print("\nSuccess: Map has been saved as 103.html")

if __name__ == "__main__":
    main()