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
water_levels = [
    {
        "geometry": wkt.loads("POINT(51.5074 -0.1278)"),  # Example coordinate for Kumbel River
        "properties": {
            "Water_level_Value": 123,
            "Date_water_level_Value": "2022-01-01",
            "Water_level_Valuecm": 123456,
            "Water_body_code": "KUM"
        }
    }
]

# Add water levels to the map
for level in water_levels:
    folium.CircleMarker(
        location=tuple(level["geometry"].coords.xy),
        radius=5,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.5,
        popup=f"Уровень воды: {level['properties']['Water_level_Value']} м\nДата: {level['properties']['Date_water_level_Value']}\nКод водного тела: {level['properties']['Water_body_code']}"
    ).add_to(m)

# Save the final map
m.save("233.html")