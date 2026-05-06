import requests
import folium
from shapely.geometry import LineString, shape
from shapely.ops import unary_union

def get_river_geometry(river_name):
    """
    Fetch river geometry from Overpass API (OpenStreetMap).
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    # Query to find ways with the specific name and waterway=river
    overpass_query = f"""
    [out:json];
    way["waterway"~"river|stream"]["name"~"{river_name}"];
    (._;);
    out geom;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()
    
    geometries = []
    for element in data.get('elements', []):
        # Extract coordinates from the geometry provided by Overpass
        coords = [(p['lon'], p['lat']) for p in element['geometry']]
        if len(coords) >= 2:
            geometries.append(LineString(coords))
    
    # Merge multiple segments of the same river into one geometry object
    if geometries:
        return unary_union(geometries)
    return None

def main():
    main_river_name = "Емель"
    potential_tributaries = ["Тентек", "Быж"]
    
    print(f"Searching for data for river {main_river_name} and its potential tributaries...")
    
    # 1. Get geometry for the main river
    main_river_geom = get_river_geometry(main_river_name)
    
    if main_river_geom is None:
        print(f"Error: Could not find geometry for {main_river_name}")
        return

    results = {}
    river_geoms = {main_river_name: main_river_geom}

    # 2. Check each potential tributary
    for trib_name in potential_tributaries:
        trib_geom = get_river_geometry(trib_name)
        if trib_geom:
            river_geoms[trib_name] = trib_geom
            # Check if the tributary intersects or touches the main river
            # We use a small buffer to account for digitization errors in OSM
            is_tributary = main_river_geom.buffer(0.001).intersects(trib_geom)
            results[trib_name] = "Yes" if is_tributary else "No"
        else:
            results[trib_name] = "Data not found"

    # Output the result
    print("\n--- Analysis Result ---")
    for river, status in results.items():
        print(f"Is {river} a tributary of {main_river_name}? {status}")

    # 3. Visualization
    # Center map around the main river
    centroid = main_river_geom.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=7, tiles='CartoDB positron')

    colors = {main_river_name: 'blue', 'Тентек': 'green', 'Быж': 'red'}

    for name, geom in river_geoms.items():
        # Handle MultiLineString or LineString
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                coords = list(line.coords)
                folium.PolyLine(coords, color=colors.get(name, 'gray'), weight=3, popup=name).add_to(m)
        elif geom.geom_type == 'LineString':
            coords = list(geom.coords)
            folium.PolyLine(coords, color=colors.get(name, 'gray'), weight=3, popup=name).add_to(m)

    # Save the map
    m.save("101.html")
    print("\nMap has been saved as 101.html")

if __name__ == "__main__":
    main()