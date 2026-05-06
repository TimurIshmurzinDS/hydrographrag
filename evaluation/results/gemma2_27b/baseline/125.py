import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, GeoJson

# Загрузка данных о расходе воды (замените на ваши файлы)
data_tekes = pd.read_csv("tekes_river_flow.csv")
data_bayankol = pd.read_csv("bayankol_river_flow.csv")

# Вычисление среднего расхода за последние 5 лет
avg_tekes = data_tekes["flow"].mean()
avg_bayankol = data_bayankol["flow"].mean()

# Вычисление отклонения от среднего для каждой реки
data_tekes["deviation"] = data_tekes["flow"] - avg_tekes
data_bayankol["deviation"] = data_bayankol["flow"] - avg_bayankol

# Определение максимального увеличения расхода
max_increase_tekes = data_tekes["deviation"].max()
max_increase_bayankol = data_bayankol["deviation"].max()

print(f"Максимальное увеличение расхода для Tekes River: {max_increase_tekes}")
print(f"Максимальное увеличение расхода для Bayankol River: {max_increase_bayankol}")

# Визуализация на карте (замените на ваши координаты)
m = Map(location=[45.0, 80.0], zoom_start=6)

# Добавление данных о реках (замените на ваши файлы GeoJson)
GeoJson("tekes_river.geojson").add_to(m)
GeoJson("bayankol_river.geojson").add_to(m)

m.save("125.html")