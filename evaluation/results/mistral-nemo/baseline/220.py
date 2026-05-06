import folium
import pandas as pd

# Шаг 1: Сбор и предварительная обработка данных
data = pd.read_csv('batareyka_river_sensors.csv') # Предполагается, что данные находятся в CSV-файле

# Шаг 2: Анализ данных (в данном примере мы просто выведем средние значения характеристик датчиков)
mean_values = data.mean()
print("Средние значения характеристик датчиков реки Batareyka:")
print(mean_values)

# Шаг 3: Проектирование корабля (в данном примере мы не будем проектировать корабль, так как это выходит за рамки возможностей Python и требует инженерных знаний)
# Вместо этого мы перейдем к шагу 4: Геопространственная визуализация

# Шаг 4: Геопространственная визуализация
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Датчик #{index+1}\nУровень воды: {row['water_level']} м\nТемпература: {row['temperature']}°C\nДавление: {row['pressure']} Па").add_to(m)

# Сохранение карты в HTML-файл
m.save("220.html")