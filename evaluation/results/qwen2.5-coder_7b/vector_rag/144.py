import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Или (пример использования географических данных)
basin_data = {
    "geometry": [wkt.loads("POLYGON((...))")],  # Пример WKT для полигонов
    "Basin_are_km²": [123456]  # Пример площади бассейна в квадратных километрах
}
basin_gdf = gpd.GeoDataFrame(basin_data, crs='EPSG:4326')

# Создание карты с центром на бассейне реки Или
centroid = basin_gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровнях воды и их датах (пример использования CSV-файла)
water_level_data = [
    {"Date_water_level_Value": "2023-10-01", "Water_level_Value": 50, "Water_quality_class": "Good"},
    {"Date_water_level_Value": "2023-10-02", "Water_level_Value": 60, "Water_quality_class": "Good"},
    # Добавьте больше данных по необходимости
]

# Визуализация данных о уровнях воды на карте
for data in water_level_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"Дата: {data['Date_water_level_Value']}, Уровень воды: {data['Water_level_Value']} м, Качество воды: {data['Water_quality_class']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("144.html")