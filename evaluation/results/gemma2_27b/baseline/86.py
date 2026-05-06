import pandas as pd
import folium

# Загрузка данных о уровнях рек из CSV файла
data = pd.read_csv("river_levels.csv")

# Определение пороговых значений для каждой реки
threshold_levels = {
    "Karaoy River": 10,
    "Temirlik River": 8,
    "Turgen River": 12
}

# Создание карты с помощью folium
m = folium.Map(location=[43.5, 76.5], zoom_start=8)

# Добавление маркеров на карту для каждой реки
for index, row in data.iterrows():
    river_name = row["River Name"]
    level = row["Level (m)"]

    if level > threshold_levels[river_name]:
        folium.Marker(location=[row["Latitude"], row["Longitude"]], popup=f"{river_name}: {level} m").add_to(m)

# Сохранение карты в HTML файл
m.save("86.html")