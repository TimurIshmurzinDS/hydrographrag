import pandas as pd
import folium

# 1. Подготовьте данные
# Предполагается, что у вас есть файл 'flood_data.csv' со столбцами 'Longitude', 'Latitude', 'Date'
data = pd.read_csv('flood_data.csv')

# 2. Загрузите данные
longitudes = data['Longitude']
latitudes = data['Latitude']
dates = data['Date']

# 3. Визуализация на карте
m = folium.Map(location=[43.2389, 76.9180], zoom_start=12)  # Начальная широта и долгота реки Ulken Almaty River

for i in range(len(longitudes)):
    folium.Marker([latitudes[i], longitudes[i]], popup=f'Date: {dates[i]}').add_to(m)

# Сохраните карту как '24.html'
m.save("24.html")