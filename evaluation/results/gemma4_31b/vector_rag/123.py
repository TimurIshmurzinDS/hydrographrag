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

    # Initialize folium Map with CartoDB positron tiles
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
        name="Basin Boundary"
    ).add_to(m)

    # Context entities: Kurty River, Sharyn River, Shyzhyn River, Sarykan River, Uzyn Kargaly River
    # Note: Coordinates (WKT) were not provided in the context, 
    # so no hardcoded point list is added here.

    # Save the final map strictly as 123.html
    m.save("123.html")
    print("Map has been successfully saved as 123.html")

if __name__ == "__main__":
    generate_hydrology_map()