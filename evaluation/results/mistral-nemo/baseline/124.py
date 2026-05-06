import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Step 1: Prepare data
data = pd.read_csv('dos_river_water_levels.csv')
dos_river_data = data[['date', 'water_level']]
dos_river_data['date'] = pd.to_datetime(dos_river_data['date'])
dos_river_data.set_index('date', inplace=True)

# Step 2: Clean data
dos_river_data.dropna(inplace=True)

# Step 3: Analyze data
X = pd.DataFrame({'year': dos_river_data.index.year})
y = dos_river_data['water_level']
model = LinearRegression()
model.fit(X, y)

# Step 4: Build regression model and predict water levels for Lepsy River in 2025
lespy_river_years = pd.DataFrame({'year': [2025]})
predicted_water_levels = model.predict(lespy_river_years)

# Step 5: Visualize results on a map using folium and save as "124.html"
m = folium.Map(location=[53.7193, 27.9505], zoom_start=8) # Starting location for Lepsy River
for year in dos_river_data.index.year:
    water_level = dos_river_data.loc[year]['water_level']
    folium.CircleMarker(location=[53.7193, 27.9505], radius=water_level/10).add_to(m)
folium.Marker([53.7193, 27.9505], popup=f'Lepsy River water level in 2025: {predicted_water_levels[0]}').add_to(m)
m.save("124.html")