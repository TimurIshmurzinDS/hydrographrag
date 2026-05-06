import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Или
basin_data = r"data/basin_data.shp"
gdf = gpd.read_file(basin_data)
gdf = gdf.to_crs('EPSG:4326')

# Получение центроидов для отображения на карте
centroid = gdf.geometry.centroid[0]

# Создание карты с центром в центре бассейна
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных (замените на реальные данные)
water_consumption_value = 1000000  # Объем воды, используемый для полива, в кубических метрах
basin_area_km2 = 5000  # Площадь бассейна в километрах квадратных

# Расчет среднего расхода воды на единицу площади
average_water_consumption_per_km2 = water_consumption_value / basin_area_km2

# Вывод результатов
print(f"Средний расход воды на единицу площади бассейна: {average_water_consumption_per_km2} м³/км²")

# Сохранение карты
m.save("39.html")