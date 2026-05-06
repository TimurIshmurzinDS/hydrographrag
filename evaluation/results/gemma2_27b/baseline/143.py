import pandas as pd
import folium

# Загрузка данных о гидропостах
data = pd.read_csv("hydroposts.csv")

# Создание карты
m = folium.Map(location=[43.2, 76.9], zoom_start=8)

# Добавление маркеров на карту
for index, row in data.iterrows():
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=f"ID: {row['ID']}, Река: {row['river']}, Состояние: {row['status']}",
        icon=folium.Icon(color="green" if row["status"] == "working" else "red")
    ).add_to(m)

# Сохранение карты
m.save("143.html")