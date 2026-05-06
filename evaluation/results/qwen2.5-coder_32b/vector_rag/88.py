import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в бассейне реки Коктал
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные данные о постах измерения уровня воды на реке Коктал
posts = [
    {"name": "Пост1", "coordinates": wkt.loads("POINT(76.95 43.25)"), "water_level_cm": 120, "date": "2023-10-01"},
    {"name": "Пост2", "coordinates": wkt.loads("POINT(77.00 43.30)"), "water_level_cm": 150, "date": "2023-10-01"},
    {"name": "Пост3", "coordinates": wkt.loads("POINT(76.98 43.28)"), "water_level_cm": 130, "date": "2023-10-01"}
]

# Добавление маркеров на карту для каждого поста
for post in posts:
    folium.Marker(
        location=[post['coordinates'].y, post['coordinates'].x],
        popup=f"Пост: {post['name']}\nУровень воды: {post['water_level_cm']} см\nДата измерения: {post['date']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("88.html")