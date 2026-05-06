import folium
import numpy as np
import random

def calculate_ndvi_from_water_level(water_level):
    """
    Эмпирическая функция для расчета прокси-индекса NDVI на основе уровня воды.
    Предполагается, что оптимальный уровень воды (например, 1.5 - 2.5 метра) 
    обеспечивает максимальный рост растительности.
    """
    # Определение оптимального уровня воды
    optimal_level = 2.0 
    # Коэффициент чувствительности
    sensitivity = 0.5
    
    # Используем функцию Гаусса для моделирования зависимости
    # NDVI = max_ndvi * exp(-(level - optimal)^2 / (2 * sigma^2))
    ndvi = 0.8 * np.exp(-((water_level - optimal_level)**2) / (2 * sensitivity**2))
    
    # Добавляем небольшое смещение, чтобы имитировать базовый уровень почвы/воды
    ndvi = ndi_adjust = ndvi - 0.1
    
    # Ограничиваем значение в диапазоне NDVI [-1, 1]
    return max(-1.0, min(1.0, ndvi))

def get_color(ndvi):
    """Возвращает цвет в зависимости от значения NDVI"""
    if ndvi > 0.5:
        return 'green'   # Густая растительность
    elif ndvi > 0.2:
        return 'yellow'  # Умеренная растительность
    else:
        return 'red'     # Отсутствие растительности или вода

# 1. Координаты примерного течения реки Талгар (Казахстан)
# Создаем несколько точек вдоль русла для демонстрации
river_points = [
    (43.21, 77.12), (43.22, 77.15), (43.23, 77.18), 
    (43.24, 77.21), (43.25, 77.24), (43.26, 77.27)
]

# 2. Генерация случайных уровней воды для каждой точки (в метрах)
water_levels = [random.uniform(0.5, 3.5) for _ in range(len(river_points))]

# 3. Инициализация карты Folium
m = folium.Map(location=[43.23, 77.20], zoom_start=12, tiles='OpenStreetMap')

# 4. Расчет NDVI и добавление маркеров на карту
for point, level in zip(river_points, water_levels):
    ndvi_val = calculate_ndvi_from_water_level(level)
    color = get_color(ndvi_val)
    
    folium.CircleMarker(
        location=point,
        radius=8,
        popup=f"Уровень воды: {level:.2f}м<br>Расчетный NDVI: {ndvi_val:.2f}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты строго в файл 270.html
m.save("270.html")

print("Modeling complete. The map has been saved as 270.html")