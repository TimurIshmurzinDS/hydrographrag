import geopandas as gpd
import folium
from shapely.geometry import Point

# Шаг 1: Сбор данных
# Предположим, у нас есть GeoDataFrame с полями сельского хозяйства и их потреблением воды (в кубометрах в год)
data = {
    'field_id': [1, 2, 3, 4],
    'geometry': [
        Point(69.085, 40.75),  # Примерные координаты полей
        Point(69.10, 40.76),
        Point(69.09, 40.77),
        Point(69.07, 40.78)
    ],
    'water_consumption': [5000, 7000, 6000, 8000]  # Потребление воды в кубометрах
}

fields_gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

# Шаг 2: Подготовка данных
# Предположим, что у нас есть данные о реках Tekeli River и Temirlik River
rivers_data = {
    'river_name': ['Tekeli River', 'Temirlik River'],
    'geometry': [
        Point(69.08, 40.75),  # Примерные координаты рек
        Point(69.12, 40.76)
    ]
}

rivers_gdf = gpd.GeoDataFrame(rivers_data, crs="EPSG:4326")

# Шаг 3: Расчет потребления воды
total_water_consumption = fields_gdf['water_consumption'].sum()
print(f"Суммарное потребление воды для сельского хозяйства: {total_water_consumption} кубометров в год")

# Шаг 4: Анализ водных ресурсов
# Здесь можно добавить более сложный анализ, но для простоты просто выведем информацию о реках

# Шаг 5: Визуализация результатов
m = folium.Map(location=[40.76, 69.08], zoom_start=12)

# Добавление полей сельского хозяйства на карту
for _, row in fields_gdf.iterrows():
    folium.CircleMarker(
        location=(row['geometry'].y, row['geometry'].x),
        radius=5,
        color='blue',
        fill=True,
        fill_color='blue',
        popup=f"Поле {row['field_id']}: {row['water_consumption']} куб.м/год"
    ).add_to(m)

# Добавление рек на карту
for _, row in rivers_gdf.iterrows():
    folium.Marker(
        location=(row['geometry'].y, row['geometry'].x),
        icon=folium.Icon(color='green'),
        popup=row['river_name']
    ).add_to(m)

# Сохранение карты в файл
m.save("107.html")