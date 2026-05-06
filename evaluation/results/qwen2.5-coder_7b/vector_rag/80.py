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

# Пример данных о расходе воды (если данные недоступны, использовать моделирование)
water_consumption_data = [
    {'river': 'Tokyraun River', 'consumption': 150},
    {'river': 'Koktal River', 'consumption': 200}
]

# Пример данных о уровне воды (если данные недоступны, использовать моделирование)
water_level_data = [
    {'river': 'Tokyraun River', 'level': 100},
    {'river': 'Koktal River', 'level': 80}
]

# Добавление маркеров на карту с данными о расходе воды
for data in water_consumption_data:
    folium.Marker([centroid.y, centroid.x], popup=f"{data['river']}: {data['consumption']} m³").add_to(m)

# Добавление маркеров на карту с данными о уровне воды
for data in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"{data['river']}: {data['level']} m").add_to(m)

# Сохранение карты в файл
m.save("80.html")