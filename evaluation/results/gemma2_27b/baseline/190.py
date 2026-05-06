import geopandas as gpd
from shapely.geometry import Polygon
import folium

# Загрузка данных о реке и сельскохозяйственных угодьях
river = gpd.read_file("river_kishi_osek.shp")
agriculture = gpd.read_file("agriculture_areas.shp")

# Определение зоны расширения
expansion_zone = river.buffer(500) # Расширение на 500 метров от реки

# Вычисление площади расширения
area_expansion = expansion_zone.area

# Предполагаемое водопотребление (в зависимости от типа культур)
water_consumption_per_hectare = 1000 # в литрах на гектар

# Расчет общего объема потребления воды
total_water_needed = area_expansion * water_consumption_per_hectare / 10000 # в кубических метрах

# Получение данных о среднем стоке реки (в кубических метрах)
average_flow = 1000000 # Предполагаемое значение, нужно заменить на реальные данные

# Сравнение водопотребления и доступности
percentage_change = total_water_needed / average_flow * 100

print(f"Процентное изменение доступных водных ресурсов: {percentage_change:.2f}%")

# Визуализация на карте (folium)
m = folium.Map(location=[43.5, 69.5], zoom_start=12) # Координаты Киши Осека

# Добавление слоя реки
folium.GeoJson(river).add_to(m)

# Добавление слоя расширения
folium.GeoJson(expansion_zone).add_to(m)

# Сохранение карты
m.save("190.html")