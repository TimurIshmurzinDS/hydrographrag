import geopandas as gpd
import folium
from shapely import wkt

# Load the basin data
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Initialize the map
m = folium.Map(location=[basin.centroid.y.mean(), basin.centroid.x.mean()], tiles='CartoDB positron')

# Add the basin to the map
folium.GeoJson(basin, name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Hardcoded list of dictionaries with water consumption data for Koktal River and Baskan River
water_consumption = [
    {"river": "Koktal River", "month": "January", "value": 100},
    {"river": "Koktal River", "month": "February", "value": 200},
    # ... add more data for Koktal River
    {"river": "Baskan River", "month": "January", "value": 150},
    {"river": "Baskan River", "month": "February", "value": 250},
    # ... add more data for Baskan River
]

# Analyze the water consumption data to identify risk of seasonal flooding
# This is a placeholder, replace with actual analysis code
risk_of_flooding = {}
for entry in water_consumption:
    if entry["river"] not in risk_of_flooding:
        risk_of_flooding[entry["river"]] = 0
    # Placeholder for risk calculation, replace with actual calculation
    risk_of_flooding[entry["river"]] += entry["value"]

# Print the calculated risks
for river, risk in risk_of_flooding.items():
    print(f"The calculated risk of seasonal flooding for {river} is: {risk}")

# Save the final map
m.save("85.html")