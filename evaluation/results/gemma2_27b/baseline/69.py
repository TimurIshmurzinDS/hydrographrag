import geopandas as gpd
import folium

# Загрузка данных о датчиках (замените на ваши файлы)
koktal_sensors = gpd.read_file("koktal_sensors.geojson")
aksu_sensors = gpd.read_file("aksu_sensors.geojson")

# Создание карты
m = folium.Map(location=[42.87, 74.59], zoom_start=10)  # Установите координаты центральной точки

# Добавление датчиков Koktal River на карту
folium.GeoJson(koktal_sensors, name="Koktal Sensors").add_to(m)

# Добавление датчиков Aksu River на карту
folium.GeoJson(aksu_sensors, name="Aksu Sensors").add_to(m)

# Сохранение карты
m.save("69.html")