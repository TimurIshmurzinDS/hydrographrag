import pandas as pd
import folium

# Загрузить данные из файла CSV
data = pd.read_csv("sensor_data.csv")

# Создать карту с помощью folium
m = folium.Map(location=[43.15, 49.2], zoom_start=12)

# Добавить маркеры на карту
for index, row in data.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Sensor ID: {row['sensor_id']}, Value: {row['value']}").add_to(m)

# Сохранить карту в файл HTML
m.save("142.html")