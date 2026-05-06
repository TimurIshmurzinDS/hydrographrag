import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о качестве воды и уровне воды (если они доступны)
water_quality_data = [
    {"name": "Shynzhaly River", "Water_quality_class": "Good"},
    {"name": "Shyzhyn River", "Water_quality_class": "Moderate"}
]

water_level_data = [
    {"name": "Shynzhaly River", "Water_level_Value": 100},
    {"name": "Shyzhyn River", "Water_level_Value": 95}
]

# Добавление меток на карту с информацией о качестве воды и уровне воды
for item in water_quality_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Quality: {item['Water_quality_class']}").add_to(m)

for item in water_level_data:
    folium.Marker([centroid.y, centroid.x], popup=f"Level: {item['Water_level_Value']}").add_to(m)

# Сохранение карты
m.save("44.html")