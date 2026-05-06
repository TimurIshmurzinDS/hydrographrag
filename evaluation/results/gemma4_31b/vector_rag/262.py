import geopandas as gpd
import folium
from shapely import wkt
import numpy as np
from sklearn.linear_model import LinearRegression

# 1. Load the basin shapefile
# Using raw string as per critical instructions
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to CRS 'EPSG:4326'
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# 2. Prediction Logic (Mock implementation of fish population prediction)
def predict_fish_population(oil_price):
    """
    Predicts fish population based on oil price.
    Hypothesis: Higher oil prices may lead to increased industrial activity 
    and potential pollution, negatively impacting fish population.
    """
    # Mock data: Oil prices (X) and Fish Population (y)
    X_train = np.array([40, 50, 60, 70, 80, 90, 100]).reshape(-1, 1)
    y_train = np.array([1000, 950, 800, 700, 600, 500, 400])
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    prediction = model.predict(np.array([[oil_price]]))
    return max(0, prediction[0])

# Example prediction for a current oil price of 75 USD
current_oil_price = 75
predicted_pop = predict_fish_population(current_oil_price)
print(f"Predicted fish population in Butak River for oil price ${current_oil_price}: {predicted_pop:.2f}")

# 3. GIS Visualization
# Initialize map using the centroid of the basin shapefile
centroid = basin_gdf.geometry.centroid
map_center = [centroid.y.iloc[0], centroid.x.iloc[0]]
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    },
    name="Butak River Basin"
).add_to(m)

# Context contains Butak village (Observation), but no WKT coordinates provided.
# If coordinates were provided, they would be added here as a hardcoded list.

# 4. Save the final map strictly as 262.html
m.save("262.html")