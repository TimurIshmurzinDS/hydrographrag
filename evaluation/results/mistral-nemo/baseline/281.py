import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
import folium

# Load historical and modern weather prediction data
historical_data = pd.read_csv('historical_data.csv')
modern_data = pd.read_csv('modern_data.csv')

# Preprocess data (remove irrelevant or duplicated records)
historical_data.dropna(inplace=True)
modern_data.dropna(inplace=True)

# Apply historical method to data and save results
historical_predictions = historical_method(historical_data)
historical_data['prediction'] = historical_predictions

# Apply modern algorithm to data and save results
modern_predictions = modern_algorithm(modern_data)
modern_data['prediction'] = modern_predictions

# Calculate accuracy metrics for both methods
historical_mae = mean_absolute_error(historical_data['actual'], historical_data['prediction'])
historical_r2 = r2_score(historical_data['actual'], historical_data['prediction'])

modern_mae = mean_absolute_error(modern_data['actual'], modern_data['prediction'])
modern_r2 = r2_score(modern_data['actual'], modern_data['prediction'])

# Print accuracy metrics
print(f"Historical Method: MAE={historical_mae}, R²={historical_r2}")
print(f"Modern Algorithm: MAE={modern_mae}, R²={modern_r2}")

# Visualize results on a map using folium
m = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

for index, row in historical_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='blue',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

for index, row in modern_data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color='red',
        fill=True,
        fill_opacity=0.5
    ).add_to(m)

m.save("281.html")