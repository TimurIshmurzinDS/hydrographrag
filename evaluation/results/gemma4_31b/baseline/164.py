import numpy as np
import pandas as pd
import folium
from scipy.stats import gumbel_r
import matplotlib.pyplot as plt

def calculate_flood_probability(data, threshold):
    """
    Вычисляет вероятность превышения порога с использованием распределения Гумбеля.
    """
    # Оценка параметров распределения Гумбеля по методу моментов
    std_dev = np.std(data)
    mean_val = np.mean(data)
    
    # Параметры для scipy.stats.gumbel_r
    # beta = std_dev * sqrt(6) / pi
    # mu = mean_val - 0.5772 * beta
    beta = std_dev * np.sqrt(6) / np.pi
    mu = mean_val - 0.57721 * beta
    
    # Вероятность того, что значение будет больше порога (1 - CDF)
    prob = 1 - gumbel_r.cdf(threshold, loc=mu, scale=beta)
    return prob

# 1. Геоданные (приблизительные координаты русел)
# Или (Ili River) - упрощенно
ili_coords = [
    [43.2, 78.5], [43.5, 80.0], [43.8, 82.0], [43.6, 84.0], [43.2, 86.0]
]
# Шынжала (Shynzhaly River) - приток
shynzhaly_coords = [
    [43.1, 81.2], [43.3, 81.5], [43.5, 81.8]
]

# 2. Генерация синтетических данных по максимальным годовым уровням воды (за 30 лет)
np.random.seed(42)
# Или: более стабильный режим
ili_data = np.random.gumbel(loc=5.0, scale=1.2, size=30) 
# Шынжала: более подвержена резким паводкам (выше вариативность)
shynzhaly_data = np.random.gumbel(loc=4.0, scale=2.5, size=30)

# Пороги экстремального паводка
threshold_ili = 8.5
threshold_shynzhaly = 8.5

# Расчет вероятностей
prob_ili = calculate_flood_probability(ili_data, threshold_ili)
prob_shynzhaly = calculate_flood_probability(shynzhaly_data, threshold_shynzhaly)

print(f"Вероятность экстремального паводка на р. Или: {prob_ili:.4f}")
print(f"Вероятность экстремального паводка на р. Шынжала: {prob_shynzhaly:.4f}")

# 3. Визуализация на карте
m = folium.Map(location=[43.5, 82.0], zoom_start=6, tiles='CartoDB positron')

def get_color(prob):
    if prob > 0.15: return 'red'
    if prob > 0.05: return 'orange'
    return 'green'

# Отрисовка р. Или
folium.PolyLine(
    ili_coords, 
    color=get_color(prob_ili), 
    weight=5, 
    opacity=0.8, 
    tooltip=f"Ili River: Prob={prob_ili:.4f}"
).add_to(m)

# Отрисовка р. Шынжала
folium.PolyLine(
    shynzhaly_coords, 
    color=get_color(prob_shynzhaly), 
    weight=5, 
    opacity=0.8, 
    tooltip=f"Shynzhaly River: Prob={prob_shynzhaly:.4f}"
).add_to(m)

# Добавление маркеров для пояснения
folium.Marker([43.5, 80.0], popup="Бассейн р. Или").add_to(m)
folium.Marker([43.3, 81.5], popup="Бассейн р. Шынжала").add_to(m)

# Сохранение карты
m.save("164.html")
print("Карта сохранена в файл 164.html")