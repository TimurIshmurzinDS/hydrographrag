import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Batareyka River
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть данные о текущем уровне воды в реке Batareyka River
# Создание списка словарей с координатами и значением уровня воды (примерные данные)
water_level_data = [
    {'coordinates': 'POINT(37.618423 55.755826)', 'date': '2023-10-01', 'level_cm': 150},
    {'coordinates': 'POINT(37.619423 55.756826)', 'date': '2023-10-02', 'level_cm': 155}
]

# Добавление маркеров на карту с данными о уровне воды
for data in water_level_data:
    point = wkt.loads(data['coordinates'])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Дата: {data['date']}, Уровень воды: {data['level_cm']} см",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("7.html")