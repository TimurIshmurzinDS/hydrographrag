import geopandas as gpd
import folium
from shapely import wkt

def main():
    # Load the basin boundary shapefile using a raw string
    # The file contains only the exterior polygon boundaries of the basin
    try:
        basin_df = gpd.read_file(r"data/basin_data.shp")
    except Exception as e:
        print(f"Error loading shapefile: {e}")
        return

    # Convert to CRS 'EPSG:4326' for compatibility with folium
    basin_df = basin_df.to_crs('EPSG:4326')

    # Calculate the centroid of the basin to initialize the map
    centroid = basin_df.geometry.centroid.iloc[0]
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
        basin_df,
        style_function=lambda x: {
            'fillColor': 'green',
            'color': 'darkgreen',
            'fillOpacity': 0.2,
            'weight': 2
        },
        name="Karaoy River Basin"
    ).add_to(m)

    # Context mentions "below the mouth of Sarysai River" as an observation point.
    # Since no specific WKT coordinates were provided in the context, 
    # we do not add hardcoded markers to avoid fabrication.
    # If WKT were present, they would be processed here.

    # Save the final map strictly as 266.html
    m.save("266.html")
    print("Map has been successfully saved as 266.html")

if __name__ == "__main__":
    main()