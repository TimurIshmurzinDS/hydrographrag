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
    data=r'{"type": "FeatureCollection", "features": [{"type": "Feature", "geometry": ' + wkt.loads(str(basin_data.geometry[0])) + ', "properties": {}}]}',
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If the context contains Coordinates (WKT), create a hardcoded list of dictionaries
hydro_features = [
    {"name": "Byzhy River", "type": "HY_HydroFeature", "properties": {"Water_level_Value": "<current_value>", "Date_water_level_Value": "<current_date>", "Water_level_Valuecm": "<current_value_in_cm>"}},
    # Add more hydro features if available
]

# Add hydro features to the map
for feature in hydro_features:
    folium.Marker(location=tuple(feature['coordinates']), popup=f"{feature['name']}\n{feature['type']}\nProperties:\n- Water_level_Value: {feature['properties']['Water_level_Value']}\n- Date_water_level_Value: {feature['properties']['Date_water_level_Value']}\n- Water_level_Valuecm: {feature['properties']['Water_level_Valuecm']}").add_to(m)

# Save the final map
m.save("63.html")