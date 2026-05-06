import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с данными о реке Шынжалы
data = pd.read_csv('shynzhal_data.csv')

# Пример структуры данных:
# date, flow_rate, water_level, temperature, consumption

# Шаг 2: Обработка данных
# Удаление пропущенных значений
data.dropna(inplace=True)

# Нормализация данных (пример)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
data[['flow_rate', 'water_level', 'temperature', 'consumption']] = scaler.fit_transform(data[['flow_rate', 'water_level', 'temperature', 'consumption']])

# Шаг 3: Моделирование изменений
# Простая линейная регрессия для примера
X = data[['consumption']]
y = data['flow_rate']
model = LinearRegression()
model.fit(X, y)

# Предсказания модели
data['predicted_flow_rate'] = model.predict(X)

# Вычисление ошибки предсказания
data['error'] = data['flow_rate'] - data['predicted_flow_rate']

# Шаг 4: Визуализация результатов
# Создание карты с использованием folium
m = folium.Map(location=[50.267, 83.196], zoom_start=10)  # Координаты примерные

# Добавление маркеров на карте для точек с наибольшей ошибкой (изменениями)
for _, row in data.nlargest(10, 'error').iterrows():
    folium.Marker(
        location=[50.267 + np.random.uniform(-0.1, 0.1), 83.196 + np.random.uniform(-0.1, 0.1)],  # Примерные координаты
        popup=f"Error: {row['error']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("36.html")