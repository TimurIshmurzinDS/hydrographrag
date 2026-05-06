import requests
import folium

def get_river_data(river_names):
    """
    Fetch river geometries from Overpass API (OpenStreetMap).
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    rivers_geo = {}
    
    for name in river_names:
        # Query to find ways with the specific name and 'waterway=river'
        query = f"""
        [out:json];
        way["name"~"{name}", i]["waterway"="river"];
        (._;);
        out geom;
        """
        response = requests.get(overpass_url, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            elements = data.get('elements', [])
            if elements:
                # Extract coordinates from the first matching element
                coords = [[point['lat'], point['lon']] for point in elements[0]['geometry']]
                rivers_geo[name] = coords
            else:
                print(f"Warning: Geometry for {name} not found.")
        else:
            print(f"Error fetching data for {name}: {response.status_code}")
            
    return rivers_geo

def assess_flood_risk(river_name):
    """
    Simulates a flood risk assessment. 
    In a production environment, this would call a hydrological API or 
    analyze real-time satellite/sensor data.
    """
    # Mock risk database
    risk_levels = {
        "Karaoy River": {"level": "High", "color": "red", "desc": "Critical water level detected"},
        "Baskan River": {"level": "Medium", "color": "orange", "desc": "Moderate risk due to recent rainfall"},
        "Temirlik River": {"level": "Low", "color": "green", "desc": "Stable water level"}
    }
    return risk_levels.get(river_name, {"level": "Unknown", "color": "gray", "desc": "No data available"})

def main():
    # List of rivers to analyze
    river_list = ["Karaoy River", "Baskan River", "Temirlik River"]
    
    print("Fetching geospatial data from OSM...")
    rivers_data = get_river_data(river_list)
    
    if not rivers_data:
        print("No river data found. Exiting.")
        return

    # Initialize map centered around the average coordinates of the found rivers
    all_coords = [coord for coords in rivers_data.values() for coord in coords]
    avg_lat = sum(p[0] for p in all_coords) / len(all_coords)
    avg_lon = sum(p[1] for p in all_coords) / len(all_coords)
    
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=7, tiles="CartoDB positron")

    print("Analyzing flood risks and generating map...")
    for river_name, coords in rivers_data.items():
        risk_info = assess_flood_risk(river_name)
        
        # Add river line to map
        folium.PolyLine(
            locations=coords,
            color=risk_info['color'],
            weight=4,
            opacity=0.8,
            tooltip=f"{river_name} - Risk: {risk_info['level']}",
            popup=f"<b>River:</b> {river_name}<br><b>Risk Level:</b> {risk_info['level']}<br><b>Status:</b> {risk_info['desc']}"
        ).add_to(m)

    # Save the map
    m.save("90.html")
    print("Success! The map has been saved as 90.html")

if __name__ == "__main__":
    main()