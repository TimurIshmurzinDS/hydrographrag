import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о уровнях воды (для демонстрации)
water_level_data = [
    {"date": "2023-01-01", "level": 150},
    {"date": "2023-02-15", "level": 160},
    {"date": "2023-03-20", "level": 170},  # Пиковый уровень
    {"date": "2023-04-10", "level": 165},
    {"date": "2023-05-01", "level": 155}
]

# Расчет пикового уровня воды и среднего многолетнего значения
peak_level = max(water_level_data, key=lambda x: x['level'])['level']
average_level = sum(item['level'] for item in water_level_data) / len(water_level_data)

print(f"Пиковый уровень воды: {peak_level} м")
print(f"Средний многолетний уровень воды: {average_level:.2f} м")

# Добавление маркеров на карту для точек измерений уровня воды
for item in water_level_data:
    folium.Marker(
        location=[centroid.y, centroid.x],  # Здесь можно использовать реальные координаты измерений
        popup=f"Дата: {item['date']}, Уровень: {item['level']} м"
    ).add_to(m)

# Сохранение карты в файл
m.save("122.html")