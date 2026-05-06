import pandas as pd
import folium

# Загрузка данных о уровне воды из CSV файла
data = pd.read_csv("river_level_data.csv")

# Определение функции для расчета потребности в поливе
def calculate_irrigation_need(water_level):
    # Здесь нужно добавить логику расчета, 
    # например, линейную модель:
    return water_level * 0.5

# Расчет потребности в поливе
data["irrigation_need"] = data["water_level"].apply(calculate_irrigation_need)

# Создание карты с помощью folium
m = folium.Map(location=[48.2, 83.1], zoom_start=10)

# Добавление данных о потреблении воды на карту
for index, row in data.iterrows():
    folium.CircleMarker(location=[row["latitude"], row["longitude"]], radius=row["irrigation_need"] * 50, color="green").add_to(m)

# Сохранение карты в HTML файл
m.save("257.html")