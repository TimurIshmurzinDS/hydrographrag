import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import folium

# 1. Simulation of Hydrological Data
np.random.seed(42)
years = np.arange(2014, 2024)
days = np.arange(1, 366)
all_days = []

# Coordinates for the rivers (approximate for simulation)
rivers_info = {
    "Koksu River": {"coords": [43.5, 80.2], "trend_factor": -0.05}, # Slight decrease
    "Byzhy River": {"coords": [43.8, 80.5], "trend_factor": 0.02}   # Slight increase
}

data_list = []

for river, info in rivers_info.items():
    for year in years:
        # Simulate daily water levels with seasonality and a trend
        # Base level + seasonal sine wave + trend * year + noise
        trend_val = info['trend_factor'] * (year - 2014)
        for day in days:
            seasonality = 2 * np.sin(2 * np.pi * day / 365)
            noise = np.random.normal(0, 0.5)
            level = 5.0 + seasonality + trend_val + noise
            data_list.append({"River": river, "Year": year, "Day": day, "Level": level})

df = pd.DataFrame(data_list)

# 2. Analysis of Minimum Levels
min_levels = df.groupby(['River', 'Year'])['Level'].min().reset_index()

results = {}
plt.figure(figsize=(12, 6))

for river in rivers_info.keys():
    river_data = min_levels[min_levels['River'] == river]
    x = river_data['Year']
    y = river_data['Level']
    
    # Linear Regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    results[river] = {"slope": slope, "p_value": p_value}
    
    # Plotting
    plt.plot(x, y, marker='o', label=f"{river} (Min Levels)")
    plt.plot(x, intercept + slope*x, '--', label=f"{river} Trend (slope={slope:.3f})")

plt.title("10-Year Trend of Minimum Water Levels")
plt.xlabel("Year")
plt.ylabel("Water Level (m)")
plt.legend()
plt.grid(True)
plt.savefig("trend_analysis.png")
plt.show()

# 3. Geospatial Visualization
# Create a map centered between the two rivers
m = folium.Map(location=[43.65, 80.35], zoom_start=8, tiles='OpenStreetMap')

for river, info in rivers_info.items():
    slope = results[river]['slope']
    trend_text = "Increasing" if slope > 0 else "Decreasing"
    color = 'green' if slope > 0 else 'red'
    
    popup_text = (f"<b>{river}</b><br>"
                  f"10-year Min Trend: {trend_text}<br>"
                  f"Slope: {slope:.4f} m/year")
    
    folium.Marker(
        location=info['coords'],
        popup=popup_text,
        icon=folium.Icon(color=color, icon='info-sign')
    ).add_to(m)

# Save the map strictly as 208.html
m.save("208.html")

print("Analysis complete. Trend plot saved as 'trend_analysis.png' and map saved as '208.html'.")