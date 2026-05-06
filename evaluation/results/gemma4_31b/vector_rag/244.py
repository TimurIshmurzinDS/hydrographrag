import geopandas as gpd
import folium
from shapely import wkt

def generate_river_map():
    # Load the shapefile using a raw string as per critical instructions
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
    center_lat = centroid.y.iloc[0]
    center_lon = centroid.x.iloc[0]

    # Initialize folium Map with specified tiles
    m = folium.Map(
        location=[center_lat, center_lon], 
        tiles='CartoDB positron', 
        zoom_start=10
    )

    # Add the basin boundary to the map
    # Using specified colors and opacity
    folium.GeoJson(
        basin_gdf, 
        fillColor='green', 
        color='darkgreen', 
        fillOpacity=0.2,
        tooltip="Basin of Dos River"
    ).add_to(m)

    # Save the final map strictly using the required filename
    m.save("244.html")

if __name__ == "__main__":
    generate_river_map()