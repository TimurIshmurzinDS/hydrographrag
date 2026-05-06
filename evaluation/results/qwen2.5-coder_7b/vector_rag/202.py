import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных временных рядов для рек Emel и Turgen (замените на реальные данные)
emel_data = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
turgen_data = [80, 120, 160, 200, 240, 280, 320, 360, 400, 440]

# Вычисление стандартного отклонения для каждого временного ряда
emel_std = (sum((x - sum(emel_data) / len(emel_data)) ** 2 for x in emel_data) / len(emel_data)) ** 0.5
turgen_std = (sum((x - sum(turgen_data) / len(turgen_data)) ** 2 for x in turgen_data) / len(turgen_data)) ** 0.5

# Определение реки с более значительной межгодовую изменчивостью стока
if emel_std > turgen_std:
    more_variable_river = "Emel River"
else:
    more_variable_river = "Turgen River"

print(f"Река {more_variable_river} демонстрирует более значительную межгодовую изменчивость стока.")

# Сохранение карты
m.save("202.html")