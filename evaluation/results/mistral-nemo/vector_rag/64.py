import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates (WKT) in the context, create a hardcoded list of dictionaries
river_coords = [
    {"name": "Tentek River", "wkt": "LINESTRING(-122.345 47.890, -122.346 47.891)"},
    # Add other rivers here if needed
]

# Create a GeoDataFrame from the river coordinates
rivers = gpd.GeoDataFrame(river_coords, geometry=[wkt.loads(coord['wkt']) for coord in river_coords])

# Add rivers to the map
for _, row in rivers.iterrows():
    folium.GeoJson(
        data=row.geometry,
        style_function=lambda x: {'color': 'blue', 'weight': 2},
    ).add_to(m)

# Save the final map
m.save("64.html")