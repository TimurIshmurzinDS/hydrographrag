import pandas as pd
import matplotlib.pyplot as plt
from folium import Map, FeatureGroup, GeoJson

# Загрузка данных
data_koksu = pd.read_csv("data_koksu.csv")
data_byzhy = pd.read_csv("data_byzhy.csv")

# Расчет минимальных уровней воды за каждый год
min_levels_koksu = data_koksu.groupby(pd.Grouper(key="date", freq="Y")).min()["level"]
min_levels_byzhy = data_byzhy.groupby(pd.Grouper(key="date", freq="Y")).min()["level"]

# Визуализация тренда
plt.plot(min_levels_koksu, label="Koksu River")
plt.plot(min_levels_byzhy, label="Byzhy River")
plt.xlabel("Year")
plt.ylabel("Minimum Water Level")
plt.legend()
plt.show()

# Картографирование
m = Map(location=[43.5, 78], zoom_start=8)
FeatureGroup(name="Rivers").add_to(m).geojson(data_koksu["geometry"])
FeatureGroup(name="Rivers").add_to(m).geojson(data_byzhy["geometry"])

# Сохранение карты
m.save("208.html")