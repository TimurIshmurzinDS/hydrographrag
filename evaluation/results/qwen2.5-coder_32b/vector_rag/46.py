import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне Сарыкан
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровне воды (для демонстрации)
water_level_data = [
    {"Date_water_level_Value": "2022-01-01", "Water_level_Value": 150, "Coordinates": wkt.loads("POINT(76.93 42.85)")},
    {"Date_water_level_Value": "2022-06-01", "Water_level_Value": 160, "Coordinates": wkt.loads("POINT(76.93 42.85)")},
    {"Date_water_level_Value": "2022-12-01", "Water_level_Value": 155, "Coordinates": wkt.loads("POINT(76.93 42.85)")},
    {"Date_water_level_Value": "2023-01-01", "Water_level_Value": 152, "Coordinates": wkt.loads("POINT(76.93 42.85)")},
    {"Date_water_level_Value": "2023-06-01", "Water_level_Value": 165, "Coordinates": wkt.loads("POINT(76.93 42.85)")},
    {"Date_water_level_Value": "2023-12-01", "Water_level_Value": 158, "Coordinates": wkt.loads("POINT(76.93 42.85)")}
]

# Фильтрация данных за 2022 и 2023 годы
water_level_2022 = [point for point in water_level_data if point["Date_water_level_Value"].startswith("2022")]
water_level_2023 = [point for point in water_level_data if point["Date_water_level_Value"].startswith("2023")]

# Добавление маркеров на карту для уровней воды за 2022 год
for point in water_level_2022:
    folium.Marker(
        location=[point["Coordinates"].y, point["Coordinates"].x],
        popup=f"Уровень воды: {point['Water_level_Value']} м (2022)",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Добавление маркеров на карту для уровней воды за 2023 год
for point in water_level_2023:
    folium.Marker(
        location=[point["Coordinates"].y, point["Coordinates"].x],
        popup=f"Уровень воды: {point['Water_level_Value']} м (2023)",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("46.html")