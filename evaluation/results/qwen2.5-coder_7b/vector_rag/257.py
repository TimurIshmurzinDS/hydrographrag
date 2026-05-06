import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне Баянколь
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о наблюдениях уровня воды (замените на реальные данные)
water_level_value = 150  # Уровень воды в метрах

# Пример данных о площади земли для полива (замените на реальные данные)
area_for_irrigation = 1000  # Площадь в гектарах

# Расчет потребности в воде
water_needed_per_hectare = 500  # Количество воды в литрах на один гектар земли
total_water_needed = area_for_irrigation * water_needed_per_hectare

print(f"Необходимое количество воды для полива: {total_water_needed} литров")

# Сохранение карты
m.save("257.html")