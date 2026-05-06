import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Пример данных (замените на реальные данные)
data = {
    'Year': [2015, 2016, 2017, 2018, 2019],
    'WaterConsumption': [100, 120, 130, 140, 150],  # в миллионах кубометров
    'WaterLevel': [1000, 980, 960, 940, 920],  # в метрах
    'PollutionIndex': [3, 4, 5, 6, 7]  # индекс загрязнения
}

df = pd.DataFrame(data)

# Анализ корреляции
correlation_matrix = df.corr()
print("Корреляционная матрица:")
print(correlation_matrix)

# Модель линейной регрессии для связи потребления воды и уровня воды
X = df[['WaterConsumption']]
y = df['WaterLevel']
model_water_level = LinearRegression().fit(X, y)
print(f"Коэффициенты модели для уровня воды: {model_water_level.coef_}, {model_water_level.intercept_}")

# Модель линейной регрессии для связи потребления воды и индекса загрязнения
X = df[['WaterConsumption']]
y = df['PollutionIndex']
model_pollution = LinearRegression().fit(X, y)
print(f"Коэффициенты модели для индекса загрязнения: {model_pollution.coef_}, {model_pollution.intercept_}")

# Визуализация на карте
m = folium.Map(location=[43.167, 80.25], zoom_start=10)

folium.Marker([43.167, 80.25], popup='Река Шынжалы').add_to(m)

# Добавление данных о потреблении воды и изменениях в экосистеме
for index, row in df.iterrows():
    folium.CircleMarker(
        location=[43.167, 80.25],
        radius=5,
        popup=f"Год: {row['Year']}, Потребление воды: {row['WaterConsumption']} Млн кубометров",
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

    folium.CircleMarker(
        location=[43.167, 80.25],
        radius=5,
        popup=f"Год: {row['Year']}, Уровень воды: {row['WaterLevel']} М",
        color='green',
        fill=True,
        fill_color='green'
    ).add_to(m)

    folium.CircleMarker(
        location=[43.167, 80.25],
        radius=5,
        popup=f"Год: {row['Year']}, Индекс загрязнения: {row['PollutionIndex']}",
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

m.save("36.html")