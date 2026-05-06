import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных о потреблении воды и их привязка к географическим координатам.
data = pd.read_csv('water_consumption_data.csv')
data['geometry'] = [(point.x, point.y) for point in data['geometry']]

# Шаг 2: Получение данных об экологических показателях для тех же местоположений.
eco_data = pd.read_csv('eco_data.csv')
merged_data = pd.merge(data, eco_data, on=['latitude', 'longitude'])

# Шаг 3: Создание модели регрессии между данными о потреблении воды и экологическими показателями.
X = merged_data[['water_consumption']]
y = merged_data['eco_indicator']
model = LinearRegression()
model.fit(X, y)

# Шаг 4: Визуализация результатов моделирования на карте с использованием библиотеки `folium`.
m = folium.Map(location=[merged_data['latitude'].mean(), merged_data['longitude'].mean()], zoom_start=8)

for _, row in merged_data.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=np.abs(model.predict([[row['water_consumption']]])[0]) * 10,
        color='blue',
        fill=True
    ).add_to(m)

m.save("36.html")