import pandas as pd
import folium

# 1. Подготовить данные
data = pd.read_csv('karatal_water_data.csv')
data['date'] = pd.to_datetime(data['date'])
data = data.set_index('date')

# 2. Проанализировать данные
optimal_time = data['flow_rate'].idxmax()
print(f'Оптимальное время для сбора воды: {optimal_time}')

# 3. Выбрать местоположение
location = (41.7509, 68.2529) # примерные координаты реки Каратал
print(f'Лучшее место для сбора воды: {location}')

# 4. Визуализация данных
m = folium.Map(location=location, zoom_start=13)

for index, row in data.iterrows():
    popup_text = f'Дата: {index}, Расход воды: {row["flow_rate"]}'
    folium.CircleMarker(location=location, radius=5, popup=popup_text).add_to(m)

m.save("214.html")