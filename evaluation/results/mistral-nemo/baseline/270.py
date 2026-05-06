import folium

# Функция для расчета площади водной поверхности реки Талгар на основе уровня воды
def calculate_water_surface_area(water_level):
    # Примерная функция для расчета площади водной поверхности реки Талгар на основе уровня воды
    return water_level ** 2 * 0.1

# Функция для расчета индекса NDVI для водной поверхности реки Талгар
def calculate_ndvi(water_surface_area):
    # Примерные значения красного и инфракрасного света для водной поверхности реки Талгар
    red_light = 0.1
    infrared_light = 0.2

    # Расчет индекса NDVI для водной поверхности реки Талгар
    ndvi = (infrared_light - red_light) / (infrared_light + red_light)

    return ndvi

# Пример использования функций для расчета индекса NDVI для реки Талгар на основе уровня воды
water_level = 5 # Примерный уровень воды в реке Талгар
water_surface_area = calculate_water_surface_area(water_level)
ndvi = calculate_ndvi(water_surface_area)

# Создание карты с помощью библиотеки folium и сохранение ее как HTML-файл
m = folium.Map(location=[43.25, 71.3], zoom_start=10) # Примерные координаты реки Талгар

# Добавление маркера на карту для реки Талгар с индексом NDVI в качестве свойства
folium.Marker([43.25, 71.3], popup=f"NDVI: {ndvi}").add_to(m)

m.save("270.html")