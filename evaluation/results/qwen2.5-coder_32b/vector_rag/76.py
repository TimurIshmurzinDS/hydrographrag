import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты гидропостов в формате WKT
hydro_posts = [
    {"name": "ГП1", "coordinates": wkt.loads("POINT(45.123 60.456)"), "water_level_cm": 150, "water_consumption_m3s": 10},
    {"name": "ГП2", "coordinates": wkt.loads("POINT(45.789 60.123)"), "water_level_cm": 180, "water_consumption_m3s": 15},
    {"name": "ГП3", "coordinates": wkt.loads("POINT(45.456 60.789)"), "water_level_cm": 200, "water_consumption_m3s": 20}
]

# Добавление гидропостов на карту
for post in hydro_posts:
    folium.Marker(
        location=[post['coordinates'].y, post['coordinates'].x],
        popup=f"ГП: {post['name']}\nУровень воды (см): {post['water_level_cm']}\nРасход воды (м³/с): {post['water_consumption_m3s']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("76.html")