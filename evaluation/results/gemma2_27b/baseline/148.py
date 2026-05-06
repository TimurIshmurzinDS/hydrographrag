import pandas as pd
from folium import Map, GeoJson

# Загрузка данных о уровнях рек (замените на ваш источник данных)
data = pd.read_csv("river_levels.csv")

# Определение порога "повышенного" уровня (замените на ваши значения)
thresholds = {
    "River A": 5,
    "River B": 3,
    "River C": 7,
}

# Фильтрация рек с повышенным уровнем
high_level_rivers = data[data["Level"] > thresholds.get(data["River"], 0)]

# Визуализация на карте (необязательно)
m = Map(location=[50, 30], zoom_start=6)

# Загрузка геоданных рек (замените на ваш файл GeoJSON)
geojson_data = GeoJson("rivers.geojson")

# Добавление слоя с реками на карту
geojson_data.add_to(m)

# Выделение рек с повышенным уровнем
for index, row in high_level_rivers.iterrows():
    river_name = row["River"]
    level = row["Level"]
    print(f"{river_name}: {level}")

# Сохранение карты
m.save("148.html")