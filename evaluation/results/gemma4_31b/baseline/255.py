import folium
import numpy as np
import matplotlib.pyplot as plt
from folium import plugins

def generate_kaskelen_relief_recipe():
    # 1. Координаты центра бассейна реки Каскелен (примерные)
    lat, lon = 43.15, 77.25
    
    # 2. Симуляция ЦМР (Digital Elevation Model) для создания текстурной карты
    # В реальном проекте здесь был бы загружен .tif файл (GeoTIFF)
    grid_size = 100
    x = np.linspace(-0.2, 0.2, grid_size)
    y = np.linspace(-0.2, 0.2, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # Создаем синтетический рельеф: горы с одной стороны, долина с другой
    # Имитация склонов Заилийского Алатау
    elevation = 1000 * np.exp(-(X**2 + Y**2)) + 500 * np.sin(X * 10) + 1500 * (X + 0.2)
    
    # 3. Определение "Рецепта текстуры" на основе высот
    # Высота -> Ингредиент
    # > 1800м: Мак (плотная текстура)
    # 1000-1800м: Кунжут (средняя текстура)
    # < 1000м: Надрезы/Мука (гладкая текстура)
    
    texture_map = []
    for row in elevation:
        row_tex = []
        for val in row:
            if val > 1800:
                row_tex.append('Poppy Seeds (High Peaks)')
            elif val > 1000:
                row_tex.append('Sesame (Slopes)')
            else:
                row_tex.append('Scoring/Flour (Valley)')
        texture_map.append(row_tex)

    # 4. Визуализация в Folium
    # Создаем карту
    m = folium.Map(location=[lat, lon], zoom_start=10, tiles='Stamen Terrain' if 'Stamen Terrain' else 'OpenStreetMap')

    # Добавляем тепловую карту, имитирующую распределение текстур (высот)
    # Генерируем точки для HeatMap на основе нашего синтетического рельефа
    heat_data = []
    for i in range(grid_size):
        for j in range(grid_size):
            # Переводим относительные координаты в географические
            point_lat = lat + y[i]
            point_lon = lon + x[j]
            weight = elevation[i, j] / 2000 # Нормализация веса
            heat_data.append([point_lat, point_lon, weight])

    plugins.HeatMap(heat_data).add_to(m)

    # Добавляем маркеры-инструкции для пекаря
    folium.Marker(
        [lat + 0.1, lon + 0.1], 
        popup="Зона Пиков: Обильно посыпать маком", 
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    folium.Marker(
        [lat, lon], 
        popup="Зона Долины: Сделать глубокий надрез вдоль русла реки", 
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

    # Сохранение карты
    m.save("255.html")
    
    print("Modeling complete. The 'Bread Texture Map' has been saved as 255.html")
    print("\n--- RECIPE GUIDE ---")
    print("1. High Elevation (Red zones on map) -> Use Poppy Seeds for rough texture.")
    print("2. Mid Elevation (Yellow zones on map) -> Use Sesame seeds for medium texture.")
    print("3. Low Elevation (Blue/Green zones on map) -> Use a blade for river-like scoring.")

if __name__ == "__main__":
    generate_kaskelen_relief_recipe()