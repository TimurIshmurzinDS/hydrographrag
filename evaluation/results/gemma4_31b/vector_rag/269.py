import geopandas as gpd
import folium
from shapely import wkt

def generate_hydrology_map():
    # Load the basin shapefile using a raw string
    # The file contains only the exterior polygon boundaries of the basin
    try:
        basin_gdf = gpd.read_file(r"data/basin_data.shp")
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return

    # Convert to CRS 'EPSG:4326' for compatibility with folium
    basin_gdf = basin_gdf.to_crs('EPSG:4326')

    # Calculate the centroid of the basin to center the map
    centroid = basin_gdf.geometry.centroid.iloc[0]
    map_center = [centroid.y, centroid.x]

    # Initialize folium Map with specified tiles
    m = folium.Map(
        location=map_center, 
        zoom_start=10, 
        tiles='CartoDB positron'
    )

    # Add the basin boundary to the map
    # Styling: fillColor='green', color='darkgreen', fillOpacity=0.2
    folium.GeoJson(
        basin_gdf,
        style_function=lambda x: {
            'fillColor': 'green',
            'color': 'darkgreen',
            'fillOpacity': 0.2,
            'weight': 2
        },
        name='Kishi Osek Basin'
    ).add_to(m)

    # Context entities: Kishi Osek River, Osek River, Observation point (1.7km above mouth)
    # Since no WKT coordinates were provided in the context, 
    # we do not add hardcoded points to avoid fabrication.
    # If coordinates were present, they would be added here as folium.Marker.

    # Save the final map strictly as 269.html
    m.save("269.html")
    print("Map successfully saved as 269.html")

if __name__ == "__main__":
    generate_hydrology_map()