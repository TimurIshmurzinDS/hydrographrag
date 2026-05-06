import folium

# Создание карты местности с центром на реке Ulken Almaty River
m = folium.Map(location=[43.2567, 71.2901], zoom_start=13)

# Получение данных о местоположении датчика и его текущем состоянии из базы данных или другого источника
sensor_location = (43.2589, 71.2912)
sensor_status = "working"  # или "not working", в зависимости от состояния датчика

# Отображение реки Ulken Almaty River на карте с помощью полигональной линии
ulken_almaty_river = [(43.2567, 71.2890), (43.2589, 71.2912), (43.2611, 71.2934)]
folium.PolyLine(ulken_almaty_river, weight=5).add_to(m)

# Отображение местоположения датчика на карте с помощью маркера
sensor_icon = folium.features.LayeredIcon(marker=folium.features.Marker(sensor_location), icon=folium.features.DivIcon(html='<div style="font-size: 20px;">Датчик</div>'))
m.add_child(sensor_icon)

# Отображение состояния датчика на карте с помощью различных цветов или значков
if sensor_status == "working":
    folium.CircleMarker(location=sensor_location, radius=5, color="green", fill=True).add_to(m)
else:
    folium.CircleMarker(location=sensor_location, radius=5, color="red", fill=True).add_to(m)

# Сохранение финальной карты в формате HTML под названием "8.html"
m.save("8.html")