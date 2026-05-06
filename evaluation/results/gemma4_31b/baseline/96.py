import requests
import geopandas as gpd
import folium
from shapely.geometry import LineString, Point
from pyproj import Transformer

def get_osm_river(river_name):
    """Fetch river geometry from Overpass API"""
    overpass_url = "http://overpass-api.de/api/interpreter"
    # Query to find ways with the specific name and waterway=river
    query = f"""
    [out:json];
    way["name"~"{river_name}"]["waterway"~"river"];
    out geom;
    """
    response = requests.get(overpass_url, params={'data': query})
    data = response.json()
    
    if not data['elements']:
        return None
    
    # Extract coordinates from the first matching element
    coords = [[point['lon'], point['lat']] for point in data['elements'][0]['geometry']]
    return LineString(coords)

def main():
    # 1. Find rivers
    print("Searching for rivers in OSM...")
    river_urzhar_geom = get_osm_river("Уржар")
    river_dos_geom = get_osm_river("Дос")

    if river_urzhar_geom is None or river_dos_geom is None:
        print("Error: One or both rivers were not found in OSM.")
        return

    # 2. Create GeoSeries for projection
    # WGS84 (EPSG:4326) -> UTM Zone 42N (EPSG:32642) for Kazakhstan
    gdf_urzhar = gpd.GeoSeries([river_urzhar_geom], crs="EPSG:4326").to_crs(epsg=32642)
    gdf_dos = gpd.GeoSeries([river_dos_geom], crs="EPSG:4326").to_crs(epsg=32642)

    # 3. Calculate minimum distance
    # .distance() in projected CRS returns meters
    min_dist = gdf_urzhar.iloc[0].distance(gdf_dos.iloc[0])
    print(f"The minimum distance between Urzhar and Dos rivers is: {min_dist:.2f} meters")

    # 4. Visualization
    # Create a map centered around the rivers
    centroid = river_urzhar_geom.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

    # Add rivers to map
    # Convert LineString to list of tuples (lat, lon)
    coords_urzhar = [(p[1], p[0]) for p in river_urzhar_geom.coords]
    coords_dos = [(p[1], p[0]) for p in river_dos_geom.coords]

    folium.PolyLine(coords_urzhar, color="blue", weight=4, label="River Urzhar").add_to(m)
    folium.PolyLine(coords_dos, color="red", weight=4, label="River Dos").add_to(m)

    # Add a legend/info
    folium.Popup(f"Distance: {min_dist:.2f} m").add_to(m)
    
    # Save the map
    m.save("96.html")
    print("Map has been saved as 96.html")

if __name__ == "__main__":
    main()