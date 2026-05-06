import pandas as pd
import folium

# Загрузка данных (пример: CSV файл)
data = pd.read_csv('kishi_almaty_river_water_level.csv')

# Предположим, что данные имеют колонки 'date' и 'water_level'
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Извлечение пикового уровня воды
peak_water_level = data['water_level'].max()
print(f"Пиковый уровень воды: {peak_water_level}")

# Вычисление среднего многолетнего показателя
mean_water_level = data['water_level'].mean()
print(f"Средний многолетний показатель уровня воды: {mean_water_level}")

# Сравнение пикового уровня с средним значением
comparison_result = "Пиковый уровень выше среднего" if peak_water_level > mean_water_level else "Пиковый уровень ниже или равен среднему"
print(f"Сравнение: {comparison_result}")

# Визуализация на карте (пример: точка на реке)
latitude, longitude = 43.2107, 76.9234  # Координаты примера точки на реке Kishi Almaty River
m = folium.Map(location=[latitude, longitude], zoom_start=15)

# Добавление маркера с информацией о пиковом уровне воды
folium.Marker(
    [latitude, longitude],
    popup=f"Пиковый уровень воды: {peak_water_level}<br>Средний многолетний показатель: {mean_water_level}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("122.html")