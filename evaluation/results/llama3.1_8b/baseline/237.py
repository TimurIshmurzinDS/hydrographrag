import folium

# Данные о координатах реки Аксу (предположим, это файл в формате GeoJSON)
river_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [48.6232, 77.0333],
                    [48.6255, 77.0357],
                    # Добавьте остальные координаты реки Аксу
                ]
            }
        }
    ]
}

# Данные о высоте воды в реке на разных участках (предположим, это файл в формате CSV)
water_level_data = {
    "data": [
        {"x": 1, "y": 2, "z": 10},  # Высота воды в метрах
        {"x": 3, "y": 4, "z": 15},
        # Добавьте остальные данные о высоте воды
    ]
}

# Создать карту с зоной затопления реки Аксу
m = folium.Map(location=[48.6250, 77.0350], zoom_start=12)

# Добавить слой для отображения реки Аксу
folium.GeoJson(river_data).add_to(m)

# Добавить слой для отображения зоны затопления
for data in water_level_data["data"]:
    folium.Circle(
        location=[data["y"], data["x"]],
        radius=data["z"] * 100,  # Преобразовать высоту в радиус круга
        color="blue",
        fill=True,
        fill_color="blue"
    ).add_to(m)

# Сохранить карту как HTML-файл
m.save("237.html")