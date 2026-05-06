import pandas as pd
import folium

# Загрузка данных о уровнях воды
data = pd.read_csv("river_levels.csv")

# Определение нормального уровня для каждой реки
normal_levels = {
    "Baskan River": 10,
    "Prokhodnaya River": 5
}

# Выделение случаев превышения нормы
exceeding_levels = data[data["level"] > normal_levels[data["river"]]]

# Создание карты с Folium
m = folium.Map(location=[45, 60], zoom_start=8)

# Добавление точек на карту для мест превышения уровня воды
for index, row in exceeding_levels.iterrows():
    folium.Marker(location=[row["latitude"], row["longitude"]], popup=f"River: {row['river']}, Level: {row['level']}").add_to(m)

# Сохранение карты
m.save("81.html")