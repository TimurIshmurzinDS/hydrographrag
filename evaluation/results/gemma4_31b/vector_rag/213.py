import geopandas as gpd
import folium
from shapely import wkt

def predict_ethereum_price(water_level, water_consumption):
    """
    Mock function to simulate the transformation of hydrological 
    sensor data into an Ethereum price forecast.
    """
    # Theoretical formula: ETH_Price = (Level * Consumption) * Constant_Factor
    constant_factor = 0.042
    forecast_price = (water_level * water_consumption) * constant_factor
    return forecast_price

# 1. Load the basin boundary shapefile
# Using raw string as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Initialize the map using the centroid of the basin
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(
    location=[centroid.y, centroid.x], 
    tiles='CartoDB positron', 
    zoom_start=10
)

# 3. Add the basin polygon to the map
folium.GeoJson(
    basin_gdf, 
    style_function=lambda x: {
        'fillColor': 'green', 
        'color': 'darkgreen', 
        'fillOpacity': 0.2
    }
).add_to(m)

# 4. Simulation of sensor data processing for Ethereum forecast
# These values represent the entities: Water_level_Valuecm and Water_consumption_Valuem³s
sensor_data = {
    "Date_water_level_Value": "2023-10-27",
    "Water_level_Valuecm": 125.5,
    "Water_consumption_Valuem³s": 12.8
}

eth_forecast = predict_ethereum_price(
    sensor_data["Water_level_Valuecm"], 
    sensor_data["Water_consumption_Valuem³s"]
)

print(f"Analysis for {sensor_data['Date_water_level_Value']}:")
print(f"Predicted Ethereum Price based on Dos River sensors: ${eth_forecast:.2f}")

# 5. Save the final map strictly as 213.html
m.save("213.html")