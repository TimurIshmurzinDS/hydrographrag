import requests
import folium
from geopy.distance import geodesic

def get_river_geometry(river_name):
    """
    Fetch river geometry from Overpass API (OpenStreetMap).
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    # Query to find the river by name and get its geometry (way)
    query = f"""
    [out:json];
    way["waterway"="river"]["name"~"{river_name}"]({
        # Approximate bounding box for Kazakhstan region to speed up/narrow search
        # but for simplicity, we search globally or by name
    });
    out geom;
    """
    # Simplified query for global search by name
    query = f'[out:json]; way["waterway"="river"]["name"="{river_name}"]; out geom;'
    
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()
    
    geometries = []
    for element in data.get('elements', []):
        # Extract coordinates from the 'geometry' field
        coords = [(point['lat'], point['lon']) for point in element['geometry']]
        geometries.append(coords)
    
    return geometries

def calculate_total_length(coords):
    """
    Calculate the total length of a line defined by coordinates in kilometers.
    """
    total_dist = 0
    for i in range(len(coords) - 1):
        total_dist += geodesic(coords[i], coords[i+1]).kilometers
    return total_dist

def main():
    river_emel_name = "Емель"
    river_karatal_name = "Каратал"

    print(f"Fetching data for {river_emel_name} and {river_karatal_name}...")
    
    emel_geoms = get_river_geometry(river_emel_name)
    karatal_geoms = get_river_geometry(river_karatal_name)

    if not emel_geoms or not karatal_geoms:
        print("Could not find one or both rivers in OSM database.")
        return

    # We take the first/longest geometry found for each river
    emel_coords = emel_geoms[0]
    karatal_coords = karatal_geoms[0]

    # 1. Calculate length of Emel
    length_emel = calculate_total_length(emel_coords)

    # 2. Check if Emel is a tributary of Karatal
    # We check if the distance between the end of Emel and any point of Karatal is very small
    is_tributary = False
    min_dist = float('inf')
    
    # Check distance from the last point of Emel to all points of Karatal
    end_point_emel = emel_coords[-1]
    for point in karatal_coords:
        dist = geodesic(end_point_emel, point).kilometers
        if dist < min_dist:
            min_dist = dist
    
    # Threshold: if the distance is less than 1km, we consider it a tributary in OSM terms
    if min_dist < 1.0:
        is_tributary = True

    print(f"Is Emel a tributary of Karatal? {'Yes' if is_tributary else 'No'}")
    print(f"Length of Emel river: {length_emel:.2f} km")

    # Visualization
    # Center map around the average of Emel's coordinates
    avg_lat = sum(p[0] for p in emel_coords) / len(emel_coords)
    avg_lon = sum(p[1] for p in emel_coords) / len(emel_coords)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=7, control_scale=True)

    # Add Karatal (Blue)
    folium.PolyLine(karatal_coords, color="blue", weight=4, opacity=0.8, 
                    tooltip=f"River {river_karatal_name}").add_to(m)
    
    # Add Emel (Red)
    folium.PolyLine(emel_coords, color="red", weight=4, opacity=0.8, 
                    tooltip=f"River {river_emel_name} (Length: {length_emel:.2f} km)").add_to(m)

    # Mark the confluence point
    folium.Marker(location=end_point_emel, 
                  popup=f"Confluence point. Dist to Karatal: {min_dist:.3f} km",
                  icon=folium.Icon(color='green')).add_to(m)

    m.save("97.html")
    print("Map saved as 97.html")

if __name__ == "__main__":
    main()