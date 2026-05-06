import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap

# Пример данных (замените на реальные данные)
data = {
    'date': ['2023-04-01', '2023-04-02', '2023-04-03', '2023-04-04'],
    'water_level': [5.2, 5.5, 6.0, 5.8],
    'temperature': [10, 12, 15, 14]
}

# Создание DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Пример моделирования (простая линейная регрессия)
from sklearn.linear_model import LinearRegression

X = df[['water_level', 'temperature']]
y = df['water_level']

model = LinearRegression()
model.fit(X, y)

# Предсказание расхода воды
df['predicted_water_level'] = model.predict(X)

# Визуализация на карте
m = folium.Map(location=[52.0896, 14.3778], zoom_start=10)  # Координаты примерного местоположения реки Tekes

# Добавление точек с данными
for index, row in df.iterrows():
    folium.Marker([52.0896, 14.3778], popup=f"Date: {row['date']}, Water Level: {row['water_level']}, Predicted: {row['predicted_water_level']}").add_to(m)

# Добавление теплового картографа (если есть координаты точек)
# heat_data = [[52.0896, 14.3778] for _ in range(len(df))]
# HeatMap(heat_data).add_to(m)

m.save("17.html")