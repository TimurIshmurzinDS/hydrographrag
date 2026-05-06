import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf = basin_gdf.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin_gdf.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_gdf.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример списка словарей с координатами и историческими данными о стоимости жилья
cities_data = [
    {"name": "Москва", "coordinates": wkt.loads("POINT(37.6173 55.7558)"), "prices": [2000, 4000, 6000, 8000, 10000]},
    {"name": "Санкт-Петербург", "coordinates": wkt.loads("POINT(30.3158 59.9391)"), "prices": [1500, 3000, 4500, 6000, 7500]},
    {"name": "Новосибирск", "coordinates": wkt.loads("POINT(82.9236 55.0302)"), "prices": [1000, 2000, 3000, 4000, 5000]},
    {"name": "Екатеринбург", "coordinates": wkt.loads("POINT(60.6057 56.8519)"), "prices": [1200, 2400, 3600, 4800, 6000]},
    {"name": "Казань", "coordinates": wkt.loads("POINT(49.1057 55.7963)"), "prices": [800, 1600, 2400, 3200, 4000]}
]

# Добавление маркеров на карту для каждого города с историческими данными о стоимости жилья
for city in cities_data:
    folium.Marker(
        location=[city["coordinates"].y, city["coordinates"].x],
        popup=f"{city['name']}<br>Цены: {', '.join(map(str, city['prices']))}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("280.html")