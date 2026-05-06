import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о качестве воды в реке Бутак
data = pd.read_csv('water_quality_data.csv')

# Пример структуры данных:
# data.columns = ['latitude', 'longitude', 'temperature', 'pH', 'pollutant_concentration']

# Шаг 2: Предобработка данных
# Удаление пропусков и нормализация данных
data.dropna(inplace=True)
features = data[['temperature', 'pH', 'pollutant_concentration']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Шаг 3: Создание модели
# Используем линейную регрессию для анализа влияния загрязнения на качество воды
X = scaled_features[:, :-1]  # Признаки (температура, pH)
y = scaled_features[:, -1]   # Целевая переменная (концентрация загрязняющих веществ)

model = LinearRegression()
model.fit(X, y)

# Предсказание уровня загрязнения
data['predicted_pollutant_concentration'] = model.predict(scaled_features[:, :-1])

# Шаг 4: Визуализация результатов
# Создание карты с помощью folium
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

# Добавление маркеров на карту
for _, row in data.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['predicted_pollutant_concentration'] * 5,  # Увеличение радиуса для наглядности
        color='red',
        fill=True,
        fill_color='red'
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("186.html")

# Вывод коэффициентов модели для анализа влияния признаков на качество воды
print("Коэффициенты модели:", model.coef_)