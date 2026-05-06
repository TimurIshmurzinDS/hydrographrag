import geopandas as gpd
import folium
from shapely import wkt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# 1. GIS Data Loading and Visualization
# Load the basin boundary shapefile using a raw string
basin_gdf = gpd.read_file(r"data/basin_data.shp")

# Convert to WGS84 CRS for folium compatibility
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Calculate centroid for map initialization
centroid = basin_gdf.geometry.centroid.iloc[0]
map_center = [centroid.y, centroid.x]

# Initialize folium map with specific tiles
m = folium.Map(location=map_center, tiles='CartoDB positron', zoom_start=10)

# Add the basin boundary to the map
folium.GeoJson(
    basin_gdf,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'darkgreen',
        'fillOpacity': 0.2,
        'weight': 2
    }
).add_to(m)

# 2. Hydrological Prediction Logic
# Mock data based on provided entities: Date_water_level_Value, Water_level_Valuecm
data = {
    'Date_water_level_Value': pd.date_range(start='2023-01-01', periods=100, freq='D'),
    'Water_level_Valuecm': np.random.normal(loc=150, scale=10, size=100).cumsum() / 10 + 150
}
df = pd.DataFrame(data)

# Prepare data for simple linear trend prediction
df['Days'] = (df['Date_water_level_Value'] - df['Date_water_level_Value'].min()).dt.days
X = df[['Days']].values
y = df['Water_level_Valuecm'].values

# Initialize and fit the model
model = LinearRegression()
model.fit(X, y)

# Predict for the next 30 days
future_days = np.array([[i] for i in range(100, 130)])
predictions = model.predict(future_days)

print(f"Prediction for Dos River water level in 30 days: {predictions[-1]:.2f} cm")

# 3. Final Map Save
# Save the final map strictly as 221.html
m.save("221.html")