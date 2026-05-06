import geopandas as gpd
from shapely.geometry import LineString
import folium

# Загрузка данных о речных путях (полилиниях)
tekes = gpd.read_file('path_to_tekes.shp')
sarykan = gpd.read_file('path_to_sarykan.shp')

# Объединение полилиний двух рек
combined_network = tekes.append(sarykan, ignore_index=True)

# Создание карты с использованием folium
m = folium.Map(location=[43.0721, 69.2851], zoom_start=6)  # Координаты примера

# Добавление полилинии объединенной сети на карту
folium.GeoJson(combined_network.geometry).add_to(m)

# Сохранение карты в файл
m.save("180.html")

print("Карта сохранена как '180.html'")