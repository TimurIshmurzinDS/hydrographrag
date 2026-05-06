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

    # Calculate the centroid of the basin to initialize the map
    centroid = basin_gdf.geometry.centroid
    mean_lat = centroid.y.mean()
    mean_lon = centroid.x.mean()

    # Initialize folium Map with CartoDB positron tiles
    m = folium.Map(
        location=[mean_lat, mean_lon], 
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
        name="Basin Boundary"
    ).add_to(m)

    # Context contains entities but no specific WKT coordinates were provided in the prompt.
    # If WKT coordinates were present, they would be added here as a hardcoded list of dictionaries.
    # Example structure if coordinates existed:
    # points = [{"name": "аул Lepsy", "coords": [lat, lon]}]
    # for pt in points:
    #     folium.Marker([pt["coords"][0], pt["coords"][1]], popup=pt["name"]).add_to(m)

    # Save the final map strictly as 210.html
    m.save("210.html")
    print("Map successfully saved as 210.html")

if __name__ == "__main__":
    generate_hydrology_map()