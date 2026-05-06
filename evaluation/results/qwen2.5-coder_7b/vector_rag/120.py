import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных для текущего уровня воды в реках (замените на реальные данные)
water_levels = [
    {'name': 'Kurty River', 'level': 150},  # Уровень воды в реке Kurty River
    {'name': 'Lepsy River', 'level': 200}   # Уровень воды в реке Lepsy River
]

# Пример данных для потребления воды сельскохозяйством (замените на реальные данные)
water_consumption = {
    'total_consumption': 500,  # Общее потребление воды сельскохозяйством
    'per_day': 100             # Потребление воды в день
}

# Определение достаточности воды для удовлетворения спроса
total_water_available = sum(item['level'] for item in water_levels)
days_to_last = total_water_available / water_consumption['per_day']

if days_to_last >= 30:
    print("Достаточно воды для удовлетворения сельскохозяйственного спроса на месяц.")
else:
    print(f"Недостаточно воды. На {days_to_last:.2f} дней будет недостаточно воды.")

# Сохранение карты
m.save("120.html")