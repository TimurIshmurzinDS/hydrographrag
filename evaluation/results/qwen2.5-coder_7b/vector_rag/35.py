import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат для ирригации (если есть)
coordinates = [
    {"name": "Plot1", "wkt": "POINT(35.1234 40.5678)"},
    {"name": "Plot2", "wkt": "POINT(35.9876 41.2345)"}
]

# Пример данных для ирригации
irrigation_data = {
    "area": 100,  # Площадь земель в гектарах
    "ETc": 0.5   # Коэффициент увлажнения (в сутки)
}

# Пример данных для реки
river_data = {
    "volume": 1000,  # Объем воды в реке в кубических метрах
    "U": 0.2        # Коэффициент использования воды
}

# Расчет потребности в воде для ирригации
Q_irrigation = irrigation_data["area"] * irrigation_data["ETc"]

# Расчет доступного количества воды в реке
Q_available = river_data["volume"] * river_data["U"]

# Расчет дефицита воды
Q_deficit = Q_irrigation - Q_available

print(f"Потребность в воде для ирригации: {Q_irrigation} м³")
print(f"Доступное количество воды в реке: {Q_available} м³")
print(f"Уровень дефицита воды для ирригации: {Q_deficit} м³")

# Сохранение карты
m.save("35.html")