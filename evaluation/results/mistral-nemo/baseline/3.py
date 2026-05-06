import pandas as pd
import folium

# Загрузка данных о уровне воды реки Talgar River
data = pd.read_csv('talgar_river_water_level.csv')

# Нахождение последнего показателя уровня воды
last_water_level = data['water_level'].iloc[-1]

# Создание карты с помощью библиотеки folium
m = folium.Map(location=[43.2568, 71.3096], zoom_start=12)  # Координаты реки Talgar River

# Добавление маркера на карту в точке последнего показателя уровня воды
folium.Marker([43.2568, 71.3096], popup=f'Последний показатель уровня воды: {last_water_level} м').add_to(m)

# Сохранение карты как HTML-файл
m.save("3.html")