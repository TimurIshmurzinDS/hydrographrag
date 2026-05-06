import pandas as pd
import folium

# Загрузить данные о показаниях датчиков
data = pd.read_csv("sensor_data.csv")

# Определить нормальный диапазон значений для каждого типа датчика
normal_ranges = {
    "temperature": (0, 30),
    "water_level": (100, 200)
}

# Выбрать неисправные датчики
defective_sensors = data[
    (data["value"] < normal_ranges[data["type"]][0]) |
    (data["value"] > normal_ranges[data["type"]][1])
]

# Создать карту с помощью folium
m = folium.Map(location=[43, 78], zoom_start=6)

# Добавить маркеры для исправных датчиков
for index, row in data.iterrows():
    if not (row["sensor_id"] in defective_sensors["sensor_id"].values):
        folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"Sensor ID: {row['sensor_id']}, Value: {row['value']}").add_to(m)

# Добавить маркеры для неисправных датчиков
for index, row in defective_sensors.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], icon=folium.Icon(color="red"), popup=f"Sensor ID: {row['sensor_id']}, Value: {row['value']}").add_to(m)

# Сохранить карту
m.save("137.html")