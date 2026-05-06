import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
import folium

# Step 1: Prepare data
data_lepsy = pd.read_csv('lepsy_river_data.csv')
data_turgen = pd.read_csv('turgen_river_data.csv')

# Step 2: Transform data (if necessary)
# ...

# Step 3: Model trends using ARIMA
model_lepsy = ARIMA(data_lepsy['water_level'], order=(5,1,0))
model_lepsy_fit = model_lepsy.fit(disp=0)

model_turgen = ARIMA(data_turgen['water_level'], order=(5,1,0))
model_turgen_fit = model_turgen.fit(disp=0)

# Step 4: Visualize results using folium
m = folium.Map(location=[data_lepsy['latitude'].mean(), data_lepsy['longitude'].mean()], zoom_start=8)

folium.Marker([data_lepsy['latitude'], data_lepsy['longitude']]).add_to(m)
folium.PolyLine(data_lespy[['latitude', 'longitude']]).add_to(m)

folium.Marker([data_turgen['latitude'], data_turgen['longitude']]).add_to(m)
folium.PolyLine(data_turgen[['latitude', 'longitude']]).add_to(m)

# Step 5: Save the final map
m.save("198.html")