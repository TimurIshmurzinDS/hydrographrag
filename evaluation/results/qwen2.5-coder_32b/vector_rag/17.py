import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Текес
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Текес
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты наблюдений (WKT) и данные о расходе воды
# Для примера создадим список словарей с данными о наблюдениях
observations = [
    {'coordinates': 'POINT(80.27 43.15)', 'discharge': 150},
    {'coordinates': 'POINT(80.30 43.16)', 'discharge': 160},
    {'coordinates': 'POINT(80.29 43.17)', 'discharge': 155},
    {'coordinates': 'POINT(80.28 43.18)', 'discharge': 165}
]

# Добавление маркеров на карту с данными о расходе воды
for obs in observations:
    point = wkt.loads(obs['coordinates'])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Расход воды: {obs['discharge']} м³/с",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("17.html")