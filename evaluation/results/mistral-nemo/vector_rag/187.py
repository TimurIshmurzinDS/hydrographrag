import geopandas as gpd
import folium
from shapely import wkt

# Load basin data and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map using folium.GeoJson
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# If there are coordinates of livestock farms in WKT format, create a list of dictionaries
farms = [
    {"name": "Farm 1", "location": wkt.loads("POINT(53.987 -6.424)")},
    {"name": "Farm 2", "location": wkt.loads("POINT(53.741 -6.022)")}
]

# Calculate potential impact of river level decrease on water consumption in each farm
for farm in farms:
    # Assuming we have data for water_level_value and water_consumption_value properties
    water_level = 100  # cm
    water_consumption = 500  # m³

    # Calculate impact based on current levels and consumption values (example calculation)
    impact = (water_level - Water_level_Valuecm) * Water_consumption_Valuem³s / water_consumption

    # Add farm location to the map with different color based on impact
    folium.Marker(
        location=farm["location"],
        popup=f"{farm['name']}: Impact {impact:.2f}",
        icon=folium.Icon(color='green' if impact < 0 else 'red')
    ).add_to(m)

# Save the final map
m.save("187.html")