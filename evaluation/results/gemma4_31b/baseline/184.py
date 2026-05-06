import numpy as np
import pandas as pd
import folium
from folium.plugins import HeatMap
import random

def generate_synthetic_gis_data(rows=50, cols=50):
    """
    Генерация синтетических данных для моделирования, так как реальные 
    растровые данные реки Киши Осек требуют доступа к специфическим API/файлам.
    """
    # Создаем сетку координат (условно вокруг реки)
    x = np.linspace(45.0, 45.1, cols) # Долгота
    y = np.linspace(55.0, 55.1, rows)  # Широта
    
    # 1. Моделируем ЦМР (DEM) - река течет по центру (минимум высоты)
    # Создаем V-образный профиль высот
    dem = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            # Высота растет по мере удаления от центральной линии (j=cols//2)
            dem[i, j] = abs(j - cols // 2) * 0.5 + random.uniform(0, 2)

    # 2. Моделируем NDVI (индекс растительности)
    # В пойме (низменности) растительность обычно выше
    ndvi = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            dist_from_center = abs(j - cols // 2)
            if dist_from_center < 5:
                ndvi[i, j] = random.uniform(0.6, 0.9) # Густая пойменная растительность
            else:
                ndvi[i, j] = random.uniform(0.2, 0.5) # Разреженная растительность

    return x, y, dem, ndvi

def calculate_sustainability(dem, ndvi):
    """
    Расчет индекса экологической устойчивости (ESI)
    """
    # Нормализация данных (0-1)
    dem_norm = (dem - np.min(dem)) / (np.max(dem) - np.min(dem))
    ndvi_norm = (ndvi - np.min(ndvi)) / (np.max(ndvi) - np.min(ndvi))
    
    # Веса: NDVI (положительный вклад), Высота (положительный вклад против затопления)
    # ESI = 0.6 * NDVI + 0.4 * DEM_norm
    esi = (0.6 * ndvi_norm) + (0.4 * dem_norm)
    return esi

def main():
    # 1. Генерация данных
    x_coords, y_coords, dem, ndvi = generate_synthetic_gis_data()
    
    # 2. Расчет устойчивости
    esi = calculate_sustainability(dem, ndvi)
    
    # 3. Подготовка данных для визуализации (список точек [lat, lon, value])
    map_data = []
    for i in range(len(y_coords)):
        for j in range(len(x_coords)):
            # Сохраняем широту, долготу и значение индекса устойчивости
            map_data.append([y_coords[i], x_coords[j], esi[i, j]])

    # 4. Создание карты Folium
    # Центр карты
    center_lat = np.mean(y_coords)
    center_lon = np.mean(x_coords)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13, tiles='OpenStreetMap')

    # Добавляем HeatMap для визуализации зон устойчивости
    # В HeatMap третье значение (weight) определяет интенсивность цвета
    HeatMap(map_data, radius=15, blur=10, min_opacity=0.4).add_to(m)

    # Добавляем информационные маркеры для демонстрации "Критических зон"
    # (Зоны с низким ESI и низкой высотой)
    critical_zones = []
    for i in range(len(y_coords)):
        for j in range(len(x_coords)):
            if esi[i, j] < 0.3 and dem[i, j] < 2:
                critical_zones.append([y_coords[i], x_coords[j]])
    
    # Ограничим количество маркеров для чистоты карты
    for point in random.sample(critical_zones, min(len(critical_zones), 10)):
        folium.CircleMarker(
            location=point,
            radius=5,
            color='red',
            fill=True,
            fill_color='red',
            popup='Зона высокого риска (Климатическая уязвимость)'
        ).add_to(m)

    # Сохранение карты
    m.save("184.html")
    print("Modeling complete. The map has been saved as 184.html")

if __name__ == "__main__":
    main()