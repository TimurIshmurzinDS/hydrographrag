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
        zoom_start=6, 
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
        name="Basin Boundary"
    ).add_to(m)

    # Context contains entities but no specific WKT coordinates for points.
    # If coordinates were provided in the context, they would be added here as a list of dictionaries.
    # Example structure if coordinates existed:
    # points = [{"name": "Emel River", "coords": [lat, lon]}, ...]
    # for pt in points:
    #     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

    # Save the final map strictly as 202.html
    m.save("202.html")
    print("Map has been successfully saved as 202.html")

if __name__ == "__main__":
    generate_hydrology_map()