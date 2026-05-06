import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границей бассейна
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Параметры модели
r = 0.1  # скорость естественного роста популяции
K = 1000  # переносимая численность популяции
N0 = 10  # начальное число особей
a = 0.5  # начальный уровень доступности корма
b = -0.001  # изменение уровня доступности корма со временем

# Моделирование роста популяции
import numpy as np
from scipy.integrate import odeint

def model(N, t):
    F = a + b * t
    dNdt = r * N * F * (1 - N / K)
    return dNdt

t = np.linspace(0, 100, 100)  # временной интервал от 0 до 100 с шагом 1
N = odeint(model, N0, t)

# Визуализация результата моделирования
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(t, N, label='Численность популяции кроликов')
plt.xlabel('Время (единицы)')
plt.ylabel('Число особей')
plt.title('Модель роста популяции кроликов в зависимости от количества корма')
plt.legend()
plt.grid(True)
plt.show()

# Сохранение карты
m.save("276.html")