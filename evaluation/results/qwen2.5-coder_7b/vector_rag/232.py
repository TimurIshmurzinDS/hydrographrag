import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центре бассейна и использованием тайла 'CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных уровня воды в реке Каскелен (в сантиметрах)
water_level_cm = 150  # Примерное значение

# Преобразование уровня воды в метры
water_level_m = water_level_cm / 100

# Добавление маркера на уровне воды в реке Каскелен
folium.Marker([centroid.y, centroid.x], popup=f"Уровень воды в реке Каскелен: {water_level_m} м").add_to(m)

# Сохранение карты
m.save("232.html")