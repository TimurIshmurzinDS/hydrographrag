import folium
import pandas as pd

# Загрузить данные о местоположении датчиков и их статусе
data = pd.read_csv('sensors_data.csv')

# Создать геоданные из данных о местоположении датчиков
geometry = [list(row) for row in zip(data['longitude'], data['latitude'])]

# Создать карту реки Talgar River с центром в координатах (43.25, 71.3)
m = folium.Map(location=[43.25, 71.3], zoom_start=10)

# Добавить местоположение датчиков на карту
for idx, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f'Status: {row["status"]}').add_to(m)

# Сохранить финальную карту как "10.html"
m.save("10.html")