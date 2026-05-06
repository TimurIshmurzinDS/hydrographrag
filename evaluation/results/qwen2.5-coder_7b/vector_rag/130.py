import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и векторных объектах
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Определение координат стока и базового уровня для каждой из рек
bayankol_river_coords = {
    "WKT": "POINT(105.123 47.456)"  # Пример WKT координаты стока Bayankol River
}

shilik_river_coords = {
    "WKT": "POINT(105.789 47.012)"  # Пример WKT координаты базового уровня Shilik River
}

# Преобразование WKT в объекты shapely.geometry.Point
bayankol_point = wkt.loads(bayankol_river_coords["WKT"])
shilik_point = wkt.loads(shilik_river_coords["WKT"])

# Вычисление отклонения стока Bayankol River относительно базового уровня Shilik River
distance = bayankol_point.distance(shilik_point)

# Визуализация результатов на карте
m = folium.Map(location=[(bayankol_point.y + shilik_point.y) / 2, (bayankol_point.x + shilik_point.x) / 2], zoom_start=10, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(basin_data.geometry.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление стока и базового уровня на карту
folium.Marker([bayankol_point.y, bayankol_point.x], popup='Bayankol River').add_to(m)
folium.Marker([shilik_point.y, shilik_point.x], popup='Shilik River').add_to(m)

# Добавление отклонения на карту
folium.CircleMarker(
    [bayankol_point.y, bayankol_point.x],
    radius=5,
    color='red',
    fill=True,
    fill_color='red',
    popup=f'Отклонение: {distance:.2f} м'
).add_to(m)

# Сохранение карты
m.save("130.html")