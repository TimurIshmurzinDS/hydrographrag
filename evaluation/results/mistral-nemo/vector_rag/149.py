import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT) for rivers Lepsy and Kish Osek
rivers_coords = [
    {"name": "Lepsy", "wkt": "LINESTRING(..."},
    {"name": "Kish Osek", "wkt": "LINESTRING(...)"}
]

# Create a function to analyze water level data for a given river
def analyze_water_level(river_name, wkt):
    # Assume that we have a pandas DataFrame 'df' with columns 'Date_water_level_Value' and 'Water_level_Value'
    # Filter data for the given river
    river_data = df[df['River'] == river_name]

    # Analyze data to find periods of no signal or constant water level
    # ...

    return periods_of_no_signal

# Loop through rivers and analyze water level data
for river in rivers_coords:
    wkt_river = wkt.loads(river['wkt'])
    folium.GeoJson(wkt_river, fillColor='blue', color='blue', fillOpacity=0.5).add_to(m)

    periods_of_no_signal = analyze_water_level(river['name'], river['wkt'])

    # Add periods of no signal to the map as red lines
    for period in periods_of_no_signal:
        folium.PolyLine(period, color='red', weight=2).add_to(m)

# Save the final map
m.save("149.html")