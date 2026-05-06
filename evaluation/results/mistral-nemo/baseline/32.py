import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('talgar_river_data.csv')

# Шаг 2: Очистка данных
data = data.dropna()
data = data[(data['water_quality'] >= 0) & (data['water_quality'] <= 10)]
data = data[(data['temperature'] >= -50) & (data['temperature'] <= 50)]
data = data[(data['river_level'] >= 0)]

# Шаг 3: Анализ данных
X = data[['industrial_activity', 'soil_quality', 'temperature', 'river_level']]
y = data['water_quality']

# Шаг 4: Моделирование
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Шаг 5: Визуализация
m = folium.Map(location=[43.2641° N, 71.3892° E], zoom_start=10)

for index, row in data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    water_quality = model.predict([[row['industrial_activity'], row['soil_quality'], row['temperature'], row['river_level']]])
    if water_quality < 5:
        color = 'green'
    elif water_quality >= 5 and water_quality < 7:
        color = 'yellow'
    else:
        color = 'red'
    folium.CircleMarker(location=[lat, lon], radius=5, color=color).add_to(m)

m.save("32.html")