import geopandas as gpd
import folium
from shapely import wkt

# Load shapefile and convert to CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Initialize folium.Map using the centroid of the shapefile
m = folium.Map(location=tuple(basin_data.centroid.xy), tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(
    data=basin_data,
    style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2},
).add_to(m)

# Hardcoded list of dictionaries for historical water level data (example)
historical_data = [
    {"Date_water_level_Value": "2010-01-01", "Water_level_Value": 5.6},
    {"Date_water_level_Value": "2011-01-01", "Water_level_Value": 4.8},
    {"Date_water_level_Value": "2012-01-01", "Water_level_Value": 6.2},
    # Add more historical data here...
]

# Calculate the mean and standard deviation of water levels
mean_wl = sum(d['Water_level_Value'] for d in historical_data) / len(historical_data)
std_dev_wl = (sum((d['Water_level_Value'] - mean_wl) ** 2 for d in historical_data) / len(historical_data)) ** 0.5

# Calculate the 50-year flood threshold
threshold_50_year_flood = mean_wl + 2 * std_dev_wl

# Calculate the probability of exceeding the 50-year flood threshold
num_exceedances = sum(1 for d in historical_data if d['Water_level_Value'] > threshold_50_year_flood)
probability_exceedance = num_exceedances / len(historical_data)

print(f"Вероятность превышения порога 50-летнего паводка для реки Коксу: {probability_exceedance:.4f}")

# Save the final map
m.save("203.html")