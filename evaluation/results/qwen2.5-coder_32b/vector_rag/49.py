import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в точке, соответствующей центроиду водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о пиковых уровнях воды (для демонстрации)
peak_levels = [
    {"date": "2015-07-15", "level": 150, "coordinates": wkt.loads("POINT(48.3 42.6)")},
    {"date": "2023-07-15", "level": 160, "coordinates": wkt.loads("POINT(48.3 42.6)")}
]

# Добавление маркеров на карту для пиковых уровней воды
for level in peak_levels:
    folium.Marker(
        location=[level['coordinates'].y, level['coordinates'].x],
        popup=f"Date: {level['date']}, Level: {level['level']} m",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("49.html")