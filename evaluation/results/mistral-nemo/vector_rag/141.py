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

# Hardcoded list of dictionaries with coordinates (WKT), date and water level value
water_level_data = [
    {'geometry': wkt.loads('POINT(55.734021 37.620893)'), 'date': '2022-01-01', 'Water_level_Value': 150},
    {'geometry': wkt.loads('POINT(55.734021 37.620893)'), 'date': '2022-01-02', 'Water_level_Value': 160},
    # Add more data points as needed
]

# Filter water level data for critical levels and plot on the map
for data_point in water_level_data:
    if data_point['Water_level_Value'] > 150:  # Example critical level threshold
        folium.CircleMarker(
            location=(data_point['geometry'].y, data_point['geometry'].x),
            radius=5,
            color='red',
            fill=True,
            fill_color='red'
        ).add_to(m)

# Save the final map
m.save("141.html")