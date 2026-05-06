import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассина и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile и использованием тайлов CartoDB positron
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=5, tiles='CartoDB positron')

# Добавление бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты Юпитера в солнечной системе (примерные данные)
jupiter_coords = {
    "type": "Point",
    "coordinates": [-89.6, -13.7]
}

# Создание геометрии из WKT
jupiter_geom = wkt.loads(wkt.dumps(jupiter_coords))

# Координаты реки Талгар (примерные данные)
talgar_coords = {
    "type": "Point",
    "coordinates": [45.123, 78.901]
}

# Создание геометрии из WKT
talgar_geom = wkt.loads(wkt.dumps(talgar_coords))

# Расчет расстояния между рекой Талгар и Юпитером (примерный расчет)
distance = talgar_geom.distance(jupiter_geom)

# Определение ингредиентов коктейля в зависимости от расстояния
if distance < 1000:
    ingredients = "Водка, лимонная сок, сахар"
elif distance >= 1000 and distance < 2000:
    ingredients = "Виски, апельсиновый сок, молоко"
else:
    ingredients = "Текила, лайм, кокосовая мята"

# Добавление информации о расстоянии и ингредиентах на карту
folium.Marker([talgar_geom.y, talgar_geom.x], popup=f"Расстояние до Юпитера: {distance:.2f} м\nИнгредиенты коктейля: {ingredients}").add_to(m)

# Сохранение карты в файл
m.save("249.html")