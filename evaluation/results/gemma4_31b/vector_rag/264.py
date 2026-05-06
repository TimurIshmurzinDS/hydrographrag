import geopandas as gpd
import folium
from shapely import wkt

def generate_hydrological_map():
    # Load the shapefile using a raw string as per strict instructions
    # The file contains only the exterior polygon boundaries of the basin
    try:
        basin_gdf = gpd.read_file(r"data/basin_data.shp")
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return

    # Convert to CRS 'EPSG:4326' for compatibility with folium
    basin_gdf = basin_gdf.to_crs('EPSG:4326')

    # Calculate the centroid of the basin to initialize the map
    centroid = basin_gdf.geometry.centroid.iloc[0]
    
    # Initialize folium Map using the centroid and specific tiles
    m = folium.Map(
        location=[centroid.y, centroid.x], 
        zoom_start=10, 
        tiles='CartoDB positron'
    )

    # Add the basin boundary to the map
    # Using strict styling: fillColor='green', color='darkgreen', fillOpacity=0.2
    folium.GeoJson(
        basin_gdf,
        style_function=lambda x: {
            'fillColor': 'green',
            'color': 'darkgreen',
            'fillOpacity': 0.2,
            'weight': 2
        },
        name="Bayankol River Basin"
    ).add_to(m)

    # Context does not provide specific WKT coordinates for points, 
    # so no hardcoded point list is added here to avoid fabrication.
    # If WKT coordinates were provided, they would be processed here.

    # Save the final map strictly using the required filename
    m.save("264.html")
    print("Map has been successfully saved as 264.html")

if __name__ == "__main__":
    generate_hydrological_map()