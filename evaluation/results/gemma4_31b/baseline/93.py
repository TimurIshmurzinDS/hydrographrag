import requests
import folium
from geopy.distance import geodesic

def get_karatal_tributaries():
    # Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass Query: 
    # 1. Find the river named 'Каратал'
    # 2. Find all ways that share a node with it and are tagged as river/stream
    query = """
    [out:json][timeout:25];
    way["name"="Каратал"]["waterway"="river"]->.main_river;
    way(bn.main_river)["waterway"~"river|stream"]->.tributaries;
    (.main_river; .tributaries;);
    out body;
    >;
    out skel pl;
    """
    
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()
    
    # Map nodes for coordinate lookup
    nodes = {node['id']: (node['lat'], node['lon']) for node in data['elements'] if node['type'] == 'node'}
    
    # Separate main river and tributaries
    rivers = []
    main_river_id = None
    
    for element in data['elements']:
        if element['type'] == 'way':
            name = element.get('tags', {}).get('name', 'Unnamed Tributary')
            coords = [nodes[node_id] for node_id in element['nodes'] if node_id in nodes]
            
            if name == "Каратал":
                main_river_id = element['id']
                rivers.append({'name': name, 'coords': coords, 'is_main': True})
            else:
                rivers.append({'name': name, 'coords': coords, 'is_main': False})
                
    return rivers

def calculate_length(coords):
    total_dist = 0
    for i in range(len(coords) - 1):
        total_dist += geodesic(coords[i], coords[i+1]).kilometers
    return total_dist

def main():
    print("Fetching data from OpenStreetMap...")
    rivers_data = get_karatal_tributaries()
    
    if not rivers_data:
        print("No data found.")
        return

    tributaries_list = []
    total_length_km = 0
    
    # Process tributaries
    for river in rivers_data:
        if not river['is_main']:
            length = calculate_length(river['coords'])
            tributaries_list.append((river['name'], length))
            total_length_km += length

    # Output results
    print("\n--- Tributaries of Karatal River ---")
    for name, length in tributaries_list:
        print(f"River: {name} | Length: {length:.2f} km")
    
    print(f"\nTotal combined length of tributaries: {total_length_km:.2f} km")

    # Visualization
    # Center map on the first coordinate of the first river found
    start_coord = rivers_data[0]['coords'][0]
    m = folium.Map(location=start_coord, zoom_start=8, tiles='CartoDB positron')

    for river in rivers_data:
        color = 'blue' if river['is_main'] else 'red'
        weight = 4 if river['is_main'] else 2
        
        folium.PolyLine(
            locations=river['coords'], 
            color=color, 
            weight=weight, 
            tooltip=river['name']
        ).add_to(m)

    m.save("93.html")
    print("\nMap has been saved as 93.html")

if __name__ == "__main__":
    main()