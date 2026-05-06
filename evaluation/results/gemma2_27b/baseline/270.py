# Библиотеки для работы с изображениями и NDVI не могут быть использованы без данных о красном и ближнем инфракрасном излучении. 
# Данный код является иллюстративным и не будет работать без соответствующих данных.

import numpy as np
from skimage import io

def calculate_ndvi(red, nir):
  """
  Рассчитывает NDVI из значений красного и ближнего инфракрасного излучения.

  Args:
    red: Массив значений красного света.
    nir: Массив значений ближнего инфракрасного света.

  Returns:
    Массив значений NDVI.
  """
  return (np.array(nir) - np.array(red)) / (np.array(nir) + np.array(red))

# Пример использования (необходимо заменить на ваши данные):
red_data = io.imread("path/to/red_image.tif") # Замените на путь к файлу с данными красного света
nir_data = io.imread("path/to/nir_image.tif") # Замените на путь к файлу с данными ближнего инфракрасного света

ndvi = calculate_ndvi(red_data, nir_data)

# Визуализация NDVI (требуется библиотека folium):
import folium

m = folium.Map() # Создаем карту

# Добавление данных NDVI на карту (необходимо адаптировать к формату ваших данных)
folium.raster_layers.ImageOverlay(ndvi, bounds=[(42.85, 74.6), (42.95, 74.7)]).add_to(m)

m.save("270.html") # Сохраняем карту