import geopandas as gpd
import folium
from shapely import wkt

# 1. Load the basin shapefile using a raw string
# The file contains only the exterior polygon boundaries of the basin
try:
    basin_gdf = gpd.read_file(r"data/basin_data.shp")
except Exception as e:
    print(f"Error loading shapefile: {e}")
    basin_gdf = None

if basin_gdf is not None:
    # Convert to CRS 'EPSG:4326' for compatibility with folium
    basin_gdf = basin_gdf.to_crs('EPSG:4326')

    # Calculate the centroid of the basin to center the map
    centroid = basin_gdf.geometry.centroid.iloc[0]
    center_lat = centroid.y
    center_lon = centroid.x

    # Initialize folium Map with specified tiles
    m = folium.Map(
        location=[center_lat, center_lon], 
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
        name="Aksu River Basin"
    ).add_to(m)

    # Note: No coordinates (WKT) were provided in the context for specific points,
    # so only the basin boundary is visualized.

    # Save the final map strictly using the required filename
    m.save("197.html")
    print("Map successfully saved as 197.html")
else:
    print("Basin data could not be processed.")