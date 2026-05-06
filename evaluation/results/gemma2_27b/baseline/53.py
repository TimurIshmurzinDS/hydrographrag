import folium
import pandas as pd

# Загрузка данных о температуре воды из CSV файла
data_2021 = pd.read_csv("temperature_2021.csv")
data_2022 = pd.read_csv("temperature_2022.csv")

# Создание карты
m = folium.Map(location=[53.8, 94.6], zoom_start=8)  # Примерные координаты реки Shilik

# Добавление точек измерения температуры на карту
for index, row in data_2021.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Температура: {row['temperature']}°C (2021)",
        icon=folium.Icon(color='blue')
    ).add_to(m)

for index, row in data_2022.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Температура: {row['temperature']}°C (2022)",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Добавление легенды
folium.Legend(title="Температура воды", colors=['blue', 'red'], labels=['2021', '2022']).add_to(m)

# Сохранение карты
m.save("53.html")