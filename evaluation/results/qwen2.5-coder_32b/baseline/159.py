import geopandas as gpd
import rasterio
from rasterio.mask import mask
import numpy as np
import folium
from shapely.geometry import mapping

# Загрузка геоданных рек и рельефа местности
lepsy_river = gpd.read_file('path_to_lepsy_river.shp')
shynzhaly_river = gpd.read_file('path_to_shynzhaly_river.shp')
dem = rasterio.open('path_to_dem.tif')

# Функция для расчета среднего уровня воды в реке
def calculate_water_level(river, dem):
    # Обрезка рельефа местности по границам реки
    out_image, out_transform = mask(dem, river.geometry, crop=True)
    # Расчет среднего значения высоты рельефа
    mean_elevation = np.mean(out_image[~np.isnan(out_image)])
    return mean_elevation

# Расчет уровня воды в реках
lepsy_level = calculate_water_level(lepsy_river, dem)
shynzhaly_level = calculate_water_level(shynzhaly_river, dem)

# Определение критических уровней для перелива (примерные значения)
critical_lepsy_level = 150  # примерный критический уровень для реки Лепсы
critical_shynzhaly_level = 160  # примерный критический уровень для реки Шынжалы

# Анализ риска перелива
lepsy_flood_risk = lepsy_level > critical_lepsy_level
shynzhaly_flood_risk = shynzhaly_level > critical_shynzhaly_level

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[42.87, 75.0], zoom_start=10)

# Добавление рек на карту
folium.GeoJson(lepsy_river).add_to(m)
folium.GeoJson(shynzhaly_river).add_to(m)

# Добавление маркеров с риском перелива
if lepsy_flood_risk:
    folium.Marker(
        location=[lepsy_river.geometry.centroid.y, lepsy_river.geometry.centroid.x],
        popup=f"Риск перелива: Да\nУровень воды: {lepsy_level} м",
        icon=folium.Icon(color='red')
    ).add_to(m)
else:
    folium.Marker(
        location=[lepsy_river.geometry.centroid.y, lepsy_river.geometry.centroid.x],
        popup=f"Риск перелива: Нет\nУровень воды: {lepsy_level} м",
        icon=folium.Icon(color='green')
    ).add_to(m)

if shynzhaly_flood_risk:
    folium.Marker(
        location=[shynzhaly_river.geometry.centroid.y, shynzhaly_river.geometry.centroid.x],
        popup=f"Риск перелива: Да\nУровень воды: {shynzhaly_level} м",
        icon=folium.Icon(color='red')
    ).add_to(m)
else:
    folium.Marker(
        location=[shynzhaly_river.geometry.centroid.y, shynzhaly_river.geometry.centroid.x],
        popup=f"Риск перелива: Нет\nУровень воды: {shynzhaly_level} м",
        icon=folium.Icon(color='green')
    ).add_to(m)

# Сохранение карты в файл
m.save("159.html")