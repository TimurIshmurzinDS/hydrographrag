import geopandas as gpd
import folium
from shapely import wkt

# Load the shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = "EPSG:4326"

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=basin_data.centroid, tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin_data, fillColor='green', color='darkgreen', fillOpacity=0.2).add_to(m)

# Hardcoded list of dictionaries for coordinates (WKT)
coordinates = [
    {'name': 'Tekes River', 'wkt': 'POLYGON((...))'},
    {'name': 'Bayankol River', 'wkt': 'POLYGON((...))'}
]

# Load river data and calculate average water consumption
for coord in coordinates:
    river_data = gpd.read_file(r"data/river_data.shp")  # Assuming river_data.shp exists with Water_consumption_Value property
    river_data = river_data[river_data['name'] == coord['name']]
    avg_water_consumption = river_data['Water_consumption_Value'].mean()

# Calculate percentage increase for each river
tekes_increase = (max(river_data['Water_consumption_Value']) - avg_water_consumption) / avg_water_consumption * 100
bayankol_increase = (max(bayankol_river_data['Water_consumption_Value']) - bayankol_avg_water_consumption) / bayankol_avg_water_consumption * 100

# Determine which river showed the greatest increase
if tekes_increase > bayankol_increase:
    greatest_increase = 'Tekes River'
else:
    greatest_increase = 'Bayankol River'

print(f"Наибольшее увеличение расхода воды по сравнению со своим средним значением за последние 5 лет показала река {greatest_increase}.")

# Save the final map
m.save("125.html")