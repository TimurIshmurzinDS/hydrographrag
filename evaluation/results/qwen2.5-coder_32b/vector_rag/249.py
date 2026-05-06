import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водной системе из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в средней точке бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Talgar Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что координаты реки Талгар известны и заданы в WKT формате
talgar_river_wkt = "POINT(76.9431 42.8542)"  # Примерные координаты города Талгар, который может быть приближен к реке
talgar_city_coords = wkt.loads(talgar_river_wkt)

# Добавление точки на карте для реки Талгар
folium.Marker([talgar_city_coords.y, talgar_city_coords.x], popup="Talgar River", icon=folium.Icon(color='blue')).add_to(m)

# Предположим координаты "Юпитера" как фиксированную точку на Земле (например, координаты города Нью-Йорка)
jupiter_coords = wkt.loads("POINT(-74.006 40.7128)")

# Вычисление расстояния между рекой Талгар и "Юпитером" в километрах
distance_km = talgar_city_coords.distance(jupiter_coords) * 111.32

# Вывод расстояния для проверки
print(f"Расстояние между рекой Талгар и 'Юпитером': {distance_km:.2f} км")

# Определение ингредиентов коктейля в зависимости от расстояния
if distance_km < 1000:
    ingredients = ["Водка", "Лимонный сок", "Сахар"]
elif distance_km < 5000:
    ingredients = ["Текила", "Ананасовый сок", "Мятная листиковая эссенция"]
else:
    ingredients = ["Красное вино", "Белый вермут", "Перец черный молотый"]

# Вывод рецепта коктейля
print("Рецепт коктейля:")
for ingredient in ingredients:
    print(f"- {ingredient}")

# Сохранение карты
m.save("249.html")