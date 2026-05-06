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

# If there are Coordinates (WKT) in the context, create a hardcoded list of dictionaries
hydro_features = [
    {"name": "Узын-Каргалы", "type": "HY_HydroFeature"},
    # Add other hydro features if available
]

# Search for the required hydro feature and extract properties
uzyn_kargaly = next((f for f in hydro_features if f['name'] == 'Узын-Каргалы'), None)
if uzyn_kargaly:
    water_consumption_value = uzyn_kargaly.get('Water_consumption_Value')
    water_consumption_valuem3s = uzyn_kargaly.get('Water_consumption_Valuem³s')

    print(f"Значения расхода воды во время весеннего паводка для реки Узын-Каргалы:\n"
          f"- Water_consumption_Value: {water_consumption_value}\n"
          f"- Water_consumption_Valuem³s: {water_consumption_valuem3s}")

# Save the final map
m.save("29.html")