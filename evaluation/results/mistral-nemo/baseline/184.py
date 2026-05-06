import numpy as np
import folium
from osgeo import gdal

# 1. Подготовка данных
def prepare_data(height_file, river_current_file, river_future_file, soil_types_file):
    # Загрузка данных о высоте над уровнем моря
    height_data = gdal.Open(height_file).ReadAsArray()

    # Загрузка данных о текущем и будущем рельефе реки Киши Осек
    river_current_data = gdal.Open(river_current_file).ReadAsArray()
    river_future_data = gdal.Open(river_future_file).ReadAsArray()

    # Загрузка данных о типах почв в пойменной зоне
    soil_types_data = gdal.Open(soil_types_file).ReadAsArray()

    return height_data, river_current_data, river_future_data, soil_types_data

# 2. Вычисление индекса экологической устойчивости
def calculate_ecological_stability(height_data, river_current_data, river_future_data, soil_types_data):
    # Пример функции вычисления индекса экологической устойчивости
    ecological_stability_index = (height_data + river_current_data + river_future_data + soil_types_data) / 4

    return ecological_stability_index

# 3. Визуализация результатов
def visualize_results(ecological_stability_index):
    # Создание карты с отображением индекса экологической устойчивости
    m = folium.Map(location=[52.7046, 25.2819], zoom_start=13)

    # Определение цветовой шкалы для индекса экологической устойчивости
    color_scale = ['green', 'yellow', 'orange', 'red']

    for i in range(ecological_stability_index.shape[0]):
        for j in range(ecological_stability_index.shape[1]):
            stability_value = ecological_stability_index[i, j]
            if stability_value < 25:
                color = color_scale[0]
            elif stability_value < 50:
                color = color_scale[1]
            elif stability_value < 75:
                color = color_scale[2]
            else:
                color = color_scale[3]

            folium.CircleMarker(location=[i, j], radius=5, color=color).add_to(m)

    # Сохранение карты в файл
    m.save("184.html")

# Основная часть кода
height_file = "path/to/height_data.tif"
river_current_file = "path/to/river_current_data.tif"
river_future_file = "path/to/river_future_data.tif"
soil_types_file = "path/to/soil_types_data.tif"

height_data, river_current_data, river_future_data, soil_types_data = prepare_data(height_file, river_current_file, river_future_data, soil_types_file)
ecological_stability_index = calculate_ecological_stability(height_data, river_current_data, river_future_data, soil_types_data)
visualize_results(ecological_stability_index)