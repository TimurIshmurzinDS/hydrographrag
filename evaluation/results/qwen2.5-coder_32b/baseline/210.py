import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import folium

# Предполагается, что у нас есть CSV файлы с историческими данными о дисcharges для Лепсы и Аксу.
# Формат данных: Дата (YYYY-MM-DD), Discharge (куб. м/с)

# Шаг 1: Сбор данных
lepsy_data = pd.read_csv('lepsy_river_discharge.csv', parse_dates=['Date'])
aksu_data = pd.read_csv('aksu_river_discharge.csv', parse_dates=['Date'])

# Шаг 2: Обработка данных
lepsy_data['Season'] = lepsy_data['Date'].dt.quarter.map({1: 'Зима', 2: 'Весна', 3: 'Лето', 4: 'Осень'})
aksu_data['Season'] = aksu_data['Date'].dt.quarter.map({1: 'Зима', 2: 'Весна', 3: 'Лето', 4: 'Осень'})

# Шаг 3: Анализ временных рядов
lepsy_seasonal_avg = lepsy_data.groupby('Season')['Discharge'].mean().reindex(['Зима', 'Весна', 'Лето', 'Осень'])
aksu_seasonal_avg = aksu_data.groupby('Season')['Discharge'].mean().reindex(['Зима', 'Весна', 'Лето', 'Осень'])

# Шаг 4: Визуализация данных
plt.figure(figsize=(12, 6))
lepsy_seasonal_avg.plot(kind='bar', color='blue', alpha=0.7, label='Река Лепса')
aksu_seasonal_avg.plot(kind='bar', color='green', alpha=0.7, label='Река Аксу')
plt.title('Сезонное распределение стока рек Лепсы и Аксу')
plt.xlabel('Сезоны')
plt.ylabel('Средний сток (куб. м/с)')
plt.legend()
plt.grid(True)
plt.show()

# Шаг 5: Географическая визуализация
# Координаты рек:
lepsy_coords = [42.8670, 79.1340]  # Примерные координаты Лепсы
aksu_coords = [42.8500, 79.1500]   # Примерные координаты Аксу

# Создание карты
m = folium.Map(location=[(lepsy_coords[0] + aksu_coords[0]) / 2, (lepsy_coords[1] + aksu_coords[1]) / 2], zoom_start=10)

# Добавление маркеров на карту с информацией о среднем стоке
folium.Marker(
    location=lepsy_coords,
    popup=f"Лепса\nСредний сток: {lepsy_seasonal_avg.mean():.2f} куб. м/с",
    icon=folium.Icon(color='blue')
).add_to(m)

folium.Marker(
    location=aksu_coords,
    popup=f"Аксу\nСредний сток: {aksu_seasonal_avg.mean():.2f} куб. м/с",
    icon=folium.Icon(color='green')
).add_to(m)

# Сохранение карты
m.save("210.html")