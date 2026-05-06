import folium

# Определение координат реки Баскан (заменить на реальные координаты)
river_coordinates = [54.7180, 39.3460]

# Загрузка данных о магазинах (заменить на реальный путь к файлу)
stores_data = folium.GeoJson("stores.geojson")

# Поиск ближайшего магазина к месту сбора льда
nearest_store = stores_data.closest(river_coordinates)

# Создание карты
m = folium.Map(location=river_coordinates, zoom_start=12)

# Добавление точки реки Баскан на карту
folium.Marker(location=river_coordinates, popup="Река Баскан").add_to(m)

# Добавление магазина на карту
folium.Marker(location=nearest_store["geometry"]["coordinates"], popup="Магазин").add_to(m)

# Рисование маршрута от реки до магазина
folium.PolyLine([river_coordinates, nearest_store["geometry"]["coordinates"]]).add_to(m)

# Сохранение карты в файл "267.html"
m.save("267.html")