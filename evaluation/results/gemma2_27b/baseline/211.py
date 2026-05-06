import pandas as pd
import folium

# Загрузка данных о уровне воды
data = pd.read_csv("water_level_uzyn_kargaly.csv")

# Преобразование уровня воды в шкалу от 0 до 1
data["normalized_level"] = (data["level"] - data["level"].min()) / (data["level"].max() - data["level"].min())

# Создание карты с помощью folium
m = folium.Map(location=[42.5, 69.5], zoom_start=10)

# Добавление данных о уровне воды на карту
for index, row in data.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=row["normalized_level"] * 10, color="blue").add_to(m)

# Сохранение карты
m.save("211.html")