import geopandas as gpd
import folium
from shapely import wkt

def calculate_satellite_orbit():
    # 1. Load the basin boundary shapefile using a raw string
    # The file contains only the exterior polygon boundaries of the basin
    basin_gdf = gpd.read_file(r"data/basin_data.shp")
    
    # Convert to WGS84 coordinate system
    basin_gdf = basin_gdf.to_crs('EPSG:4326')
    
    # Calculate centroid for map initialization
    centroid = basin_gdf.geometry.centroid
    center_lat = centroid.y.iloc[0]
    center_lon = centroid.x.iloc[0]
    
    # 2. Initialize folium Map
    m = folium.Map(
        location=[center_lat, center_lon], 
        tiles='CartoDB positron', 
        zoom_start=10
    )
    
    # 3. Add the basin boundary to the map
    folium.GeoJson(
        basin_gdf, 
        style_function=lambda x: {
            'fillColor': 'green', 
            'color': 'darkgreen', 
            'fillOpacity': 0.2
        }
    ).add_to(m)
    
    # 4. Define observation points based on context
    # Since WKT coordinates were not provided in the text context, 
    # we define a representative point for the "0.2 km above confluence" 
    # relative to the basin centroid to simulate the orbit calculation.
    observations = [
        {
            "name": "Observation: 0.2 km above confluence with Osek River",
            "coords": [center_lat + 0.01, center_lon + 0.01]
        }
    ]
    
    # Add observation points to map
    for obs in observations:
        folium.Marker(
            location=obs["coords"], 
            popup=obs["name"], 
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    # 5. Simulate Satellite Orbit (Ground Track)
    # We create a linear path crossing the basin to represent the satellite orbit
    orbit_path = [
        [center_lat - 0.1, center_lon - 0.1], 
        [center_lat + 0.1, center_lon + 0.1]
    ]
    
    folium.PolyLine(
        orbit_path, 
        color="red", 
        weight=2.5, 
        opacity=0.8, 
        tooltip="Satellite Ground Track"
    ).add_to(m)
    
    # 6. Save the final map strictly as 250.html
    m.save("250.html")

if __name__ == "__main__":
    calculate_satellite_orbit()