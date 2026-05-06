import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap
import numpy as np

# Шаг 1: Сбор и анализ данных о реке Аягоз.
data = {
    'дата': ['2022-01-01', '2022-02-01', '2022-03-01'],
    'объем_воды': [100, 120, 150],
    'скорость_течения': [1.5, 1.8, 2.0]
}
df = pd.DataFrame(data)

# Шаг 2: Определение сезонных изменений реки.
seasonal_changes = df.groupby('дата')['объем_воды'].mean().reset_index()

# Шаг 3: Создание геообъектов для представления ракеты и ее компонентов.
rocket_components = {
    'двигатель': [40.0, 60.0],
    'топливо': [30.0, 50.0],
    'навигационная_система': [20.0, 40.0]
}
df_rocket = pd.DataFrame(rocket_components)

# Шаг 4: Использование алгоритмов машинного обучения для определения оптимальных параметров ракеты.
from sklearn.linear_model import LinearRegression
X = seasonal_changes['объем_воды'].values.reshape(-1, 1)
y = df_rocket['двигатель'].values
model = LinearRegression()
model.fit(X, y)

# Шаг 5: Визуализация результатов моделирования на карте.
m = Map(location=[40.0, 60.0], zoom_start=10)
HeatMap(data=df[['объем_воды', 'скорость_течения']].values, radius=20).add_to(m)

# Добавление маркеров для представления ракеты и ее компонентов.
for i in range(len(df_rocket)):
    Marker(location=df_rocket.iloc[i][0:2], popup='Двигатель').add_to(m)
    Marker(location=df_rocket.iloc[i][0:2] + [10, 10], popup='Топливо').add_to(m)

# Сохранение карты в файл.
m.save("228.html")