import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile и использованием тайлов 'CartoDB positron'
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о текущих уровнях воды в реках Лепсы и Бутак (замените на реальные данные)
water_levels = [
    {"river": "Лепса", "level": 150, "date": "2023-10-01"},
    {"river": "Бутак", "level": 145, "date": "2023-10-01"}
]

# Добавление маркеров на карту с уровнями воды
for level in water_levels:
    folium.Marker([centroid.y, centroid.x], popup=f"{level['river']}: {level['level']} м", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("138.html")