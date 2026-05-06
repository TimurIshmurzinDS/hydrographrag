import folium
from shapely.geometry import LineString, Point

# 1. Координаты реки Талгар (упрощенный маршрут для моделирования)
# Приблизительные координаты течения реки в предгорьях Заилийского Алатау
talgar_river_coords = [
    [43.1500, 78.1000], 
    [43.1200, 78.1500], 
    [43.0800, 78.2000], 
    [43.0500, 78.2500], 
    [43.0200, 78.3000]
]

# 2. Создание объекта LineString для анализа
river_line = LineString(talgar_river_coords)

# 3. Определение точек сбора ингредиентов (в пределах воображаемого буфера)
# Точки: [Широта, Долгота, Название ингредиента]
ingredients_points = [
    [43.1350, 78.1300, "Дикая Мята"],
    [43.0650, 78.2200, "Горный Чабрец"],
    [43.0300, 78.2800, "Дикая Малина (листья)"]
]

# Точка забора воды
water_source = [43.1000, 78.1800]

# Точка приготовления (Camp)
cooking_site = [43.0800, 78.2000]

# Инициализация карты Folium
m = folium.Map(location=[43.08, 78.20], zoom_start=11, tiles="OpenStreetMap")

# Визуализация русла реки
folium.PolyLine(
    talgar_river_coords, 
    color="blue", 
    weight=5, 
    opacity=0.8, 
    tooltip="Река Талгар"
).add_to(m)

# Визуализация "Буферной зоны сбора" (упрощенно кругами вокруг реки)
for coord in talgar_river_coords:
    folium.Circle(
        location=coord, 
        radius=2000, 
        color="green", 
        fill=True, 
        fill_opacity=0.1, 
        tooltip="Зона сбора ингредиентов"
    ).add_to(m)

# Добавление маркеров ингредиентов
for pt in ingredients_points:
    folium.Marker(
        location=[pt[0], pt[1]], 
        popup=f"Сбор: {pt[2]}", 
        icon=folium.Icon(color="green", icon="leaf")
    ).add_to(m)

# Добавление маркера источника воды
folium.Marker(
    location=water_source, 
    popup="Источник воды из р. Талгар", 
    icon=folium.Icon(color="blue", icon="tint")
).add_to(m)

# Добавление маркера места приготовления
folium.Marker(
    location=cooking_site, 
    popup="Место приготовления блюда", 
    icon=folium.Icon(color="red", icon="fire")
).add_to(m)

# Сохранение карты
m.save("256.html")

print("Modeling complete. The map has been saved as 256.html.")
print("Recipe: 'Mountain Infusion of Talgar' based on geospatial resource analysis.")