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
hydro_features = [
    {"name": "Tokyraun River", "type": "HY_HydroFeature"},
    {"name": "Koktal River", "type": "HY_HydroFeature"}
]

# Add rivers to the map
for feature in hydro_features:
    river_name = feature['name']
    river_type = feature['type']

    # Assume that water consumption data is available for these rivers
    water_consumption_value = f"Water consumption value for {river_name}"

    folium.Marker(location=(0, 0), popup=f"{river_name}\n{river_type}\n{water_consumption_value}").add_to(m)

# Save the final map
m.save("80.html")