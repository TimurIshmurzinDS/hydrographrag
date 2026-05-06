import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries containing coordinates (WKT)
coordinates = [
    {'year': 2022, 'date': '2022-01-01', 'water_level': 5.6},
    {'year': 2022, 'date': '2022-02-01', 'water_level': 5.8},
    {'year': 2023, 'date': '2023-01-01', 'water_level': 6.2},
    {'year': 2023, 'date': '2023-02-01', 'water_level': 6.5}
]

# Filter data by year and calculate average water level
avg_water_level_2022 = sum([coord['water_level'] for coord in coordinates if coord['year'] == 2022]) / len([coord for coord in coordinates if coord['year'] == 2022])
avg_water_level_2023 = sum([coord['water_level'] for coord in coordinates if coord['year'] == 2023]) / len([coord for coord in coordinates if coord['year'] == 2023])

# Compare average water levels
if avg_water_level_2022 > avg_water_level_2023:
    print("Уровень воды в реке Sarykan River в 2022 году был выше, чем в 2023 году.")
elif avg_water_level_2022 < avg_water_level_2023:
    print("Уровень воды в реке Sarykan River в 2023 году был выше, чем в 2022 году.")
else:
    print("Уровни воды в реке Sarykan River в 2022 и 2023 годах были одинаковыми.")

# Save the final map
m.save("46.html")