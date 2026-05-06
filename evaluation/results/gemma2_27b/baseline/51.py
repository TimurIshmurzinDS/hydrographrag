import pandas as pd
import folium

# 1. Получение данных (замените 'data.csv' на фактический путь к файлу)
data = pd.read_csv('data.csv', parse_dates=['date'])

# 2. Предобработка данных
data['season'] = data['date'].dt.quarter.apply(lambda x: 'Summer' if x in [2, 3] else 'Winter')
summer_avg = data[data['season'] == 'Summer']['flow'].mean()
winter_avg = data[data['season'] == 'Winter']['flow'].mean()

# 3. Визуализация
m = folium.Map(location=[54.0, 62.0], zoom_start=8)  # Примерные координаты реки Kurty River

folium.Marker([54.0, 62.0], popup=f"Средний расход летом: {summer_avg:.2f}").add_to(m)
folium.Marker([54.1, 62.1], popup=f"Средний расход зимой: {winter_avg:.2f}").add_to(m)

# Сохранение карты
m.save("51.html")