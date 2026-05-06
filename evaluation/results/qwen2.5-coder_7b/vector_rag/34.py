import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы реки Лепси из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центре границы реки
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы реки на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о качестве воды (замените на реальные данные)
water_quality_data = [
    {'lat': 56.1234, 'lon': 87.5678, 'quality_class': 'II'},
    {'lat': 56.1235, 'lon': 87.5679, 'quality_class': 'III'},
    {'lat': 56.1236, 'lon': 87.5680, 'quality_class': 'I'}
]

# Добавление маркеров с информацией о качестве воды
for point in water_quality_data:
    folium.Marker(
        location=[point['lat'], point['lon']],
        popup=f"Класс качества воды: {point['quality_class']}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("34.html")