import folium
import pandas as pd

# Загрузить данные о датчиках из CSV файла
data = pd.read_csv("sensors.csv")

# Создать карту с центром в регионе
m = folium.Map(location=[45, 30], zoom_start=8)

# Добавить маркеры на карту
for index, row in data.iterrows():
    if row["status"] == "working":
        folium.Marker(location=[row["latitude"], row["longitude"]], popup=row["name"], icon=folium.Icon(color="green")).add_to(m)
    else:
        folium.Marker(location=[row["latitude"], row["longitude"]], popup=row["name"], icon=folium.Icon(color="red")).add_to(m)

# Сохранить карту в HTML файл
m.save("136.html")