import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
if True:
    tributaries = [
        {"name": "Uzyn Kargaly River", "coordinates": wkt.loads("POINT(74.56 43.29)")},
        # Add more tributaries here if available
    ]

# Add tributaries to the map using folium.CircleMarker
for trib in tributaries:
    folium.CircleMarker(
        location=trib["coordinates"].y, radius=5,
        popup=f"{trib['name']}\nCoordinates: {trib['coordinates'].wkt}",
        color='red',
    ).add_to(m)

# Save the final map
m.save("91.html")