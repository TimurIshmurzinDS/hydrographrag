import numpy as np
import folium
import random
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """Вычисление расстояния между двумя точками в километрах"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Радиус Земли
    return c * r

def generate_shilik_river_model():
    # 1. Координаты примерного участка реки Шилик (Казахстан/Китай)
    start_coords = (44.12, 80.50) # Lat, Lon
    end_coords = (44.50, 84.20)   # Lat, Lon
    
    num_points = 100
    lats = np.linspace(start_coords[0], end_coords[0], num_points)
    lons = np.linspace(start_coords[1], end_coords[1], num_points)
    
    # 2. Моделирование извилистости (добавление синусоидального смещения и шума)
    amplitude = 0.15 # Амплитуда меандрирования
    frequency = 10   # Частота изгибов
    
    # Создаем смещение относительно базовой линии
    offsets = amplitude * np.sin(np.linspace(0, 2 * np.pi * frequency, num_points)) 
    offsets += np.random.normal(0, 0.05, num_points) # Добавляем случайный шум
    
    # Применяем смещение к долготе (упрощенно для визуализации)
    river_path = []
    for i in range(num_points):
        river_path.append([lats[i] + offsets[i]*0.1, lons[i] + offsets[i]])

    # 3. Расчет коэффициента извилистости (Sinuosity)
    actual_length = 0
    for i in range(len(river_path) - 1):
        actual_length += haversine(river_path[i][1], river_path[i][0], 
                                  river_path[i+1][1], river_path[i+1][0])
    
    straight_length = haversine(start_coords[1], start_coords[0], 
                               end_coords[1], end_coords[0])
    
    sinuosity_index = actual_length / straight_length
    print(f"Calculated Sinuosity Index (S): {sinuosity_index:.4f}")

    # 4. Генерация случайных чисел на основе извилистости
    # Используем S как множитель для генерации значений (например, уровень заиления)
    random_values = [round(random.uniform(0, 100) * sinuosity_index, 2) for _ in range(num_points)]
    
    return river_path, random_values, sinuosity_index

# --- Execution ---
river_path, random_values, s_index = generate_shilik_river_model()

# 5. Визуализация на карте
# Центр карты
m = folium.Map(location=[44.3, 82.3], zoom_start=6, tiles='OpenStreetMap')

# Рисуем русло реки
folium.PolyLine(river_path, color="blue", weight=3, opacity=0.8, tooltip="Русло реки Шилик").add_to(m)

# Добавляем точки сгенерированных случайных чисел
for i in range(0, len(river_path), 5): # Ставим маркеры каждые 5 точек для чистоты карты
    folium.CircleMarker(
        location=river_path[i],
        radius=5,
        popup=f"Value: {random_values[i]}",
        color="red",
        fill=True,
        fill_color="red"
    ).add_to(m)

# Сохранение карты
m.save("254.html")
print("Modeling complete. Map saved as 254.html")