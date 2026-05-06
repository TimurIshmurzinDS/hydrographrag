import pandas as pd
import folium

# Шаг 1: Сбор данных (предположим, что данные находятся в файле 'water_levels.csv')
data = pd.read_csv('water_levels.csv')

# Шаг 2: Обработка данных - фильтрация по названию реки и сортировка по дате
talgar_data = data[data['river_name'] == 'Talgar River']
latest_water_level = talgar_data.sort_values(by='date', ascending=False).iloc[0]

# Вывод последнего показателя уровня воды
print(f"Последний показатель уровня воды на реке Talgar River: {latest_water_level['water_level']}")

# Шаг 3: Визуализация данных на карте (координаты примерные, замените их реальными)
m = folium.Map(location=[42.8605, 71.3965], zoom_start=10)  # Координаты Бишкека, Кыргызстан

# Добавление маркера с последним показателем уровня воды
folium.Marker(
    location=[42.8605, 71.3965],  # Замените на реальные координаты реки Talgar River
    popup=f"Последний уровень воды: {latest_water_level['water_level']}",
    icon=folium.Icon(color='blue')
).add_to(m)

# Шаг 4: Сохранение карты в файл
m.save("3.html")