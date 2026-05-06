import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровнях воды (заменить на реальные данные)
water_level_data = [
    {"date": "2023-01-01", "value_cm": 150},
    {"date": "2023-02-01", "value_cm": 160},
    # Добавить остальные точки данных
]

# Пример визуализации точек уровня воды (заменить на реальную логику прогнозирования)
for point in water_level_data:
    folium.Marker(
        location=[centroid.y, centroid.x],  # Заменить на реальные координаты
        popup=f"Дата: {point['date']}, Уровень воды: {point['value_cm']} см",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("124.html")