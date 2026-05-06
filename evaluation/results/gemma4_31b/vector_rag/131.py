import geopandas as gpd
import folium
from shapely import wkt

def generate_hydrology_map():
    # Load the shapefile using a raw string as per strict instructions
    # The file contains only the exterior polygon boundaries of the basin
    try:
        basin_gdf = gpd.read_file(r"data/basin_data.shp")
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return

    # Convert to CRS 'EPSG:4326' for compatibility with folium
    basin_gdf = basin_gdf.to_crs('EPSG:4326')

    # Calculate the centroid of the basin to initialize the map center
    centroid = basin_gdf.geometry.centroid
    mean_lat = centroid.y.mean()
    mean_lon = centroid.x.mean()

    # Initialize folium Map with specified tiles
    m = folium.Map(
        location=[mean_lat, mean_lon], 
        zoom_start=8, 
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
        name="Hydrological Basin"
    ).add_to(m)

    # Note: No coordinates (WKT) were provided in the context for specific rivers,
    # so only the basin boundary is visualized. 
    # If WKTs were present, they would be added here as hardcoded markers.

    # Save the final map strictly using the required filename
    m.save("131.html")
    print("Map successfully saved as 131.html")

if __name__ == "__main__":
    generate_hydrology_map()