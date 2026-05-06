import numpy as np
import folium
from folium.plugins import HeatMap

# Параметры модели
N0 = 10  # Начальное количество кроликов на каждой ячейке
r = 0.2  # Коэффициент роста популяции
T = 10   # Количество временных шагов для моделирования

# Создание примерного растра количества корма (например, 10x10)
np.random.seed(42)
feed_raster = np.random.randint(50, 200, size=(10, 10))  # Количество корма на каждой ячейке

# Инициализация популяции кроликов
rabbit_population = np.full_like(feed_raster, N0)

# Моделирование роста популяции кроликов
for t in range(T):
    K = feed_raster / 10  # Несущая способность среды зависит от количества корма
    rabbit_population = rabbit_population + r * rabbit_population * (1 - rabbit_population / K)
    rabbit_population[rabbit_population < 0] = 0  # Устранение отрицательных значений

# Создание карты с начальным распределением популяции кроликов
m = folium.Map(location=[55.75, 37.62], zoom_start=10)  # Координаты Москвы для примера

# Начальное распределение популяции кроликов
initial_data = [(i, j, rabbit_population[i, j]) for i in range(10) for j in range(10)]
HeatMap(initial_data, radius=15).add_to(m)

# Конечное распределение популяции кроликов
final_data = [(i, j, rabbit_population[i, j]) for i in range(10) for j in range(10)]
folium.plugins.HeatMap(final_data, radius=15, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(m)

# Сохранение карты
m.save("276.html")