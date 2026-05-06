import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для визуализации)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=8, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о водном уровне в реках (замените на реальные данные)
water_level_data = [
    {'river': 'Ili River', 'season': 'winter', 'level': 150},
    {'river': 'Ili River', 'season': 'spring', 'level': 200},
    {'river': 'Ili River', 'season': 'summer', 'level': 300},
    {'river': 'Ili River', 'season': 'autumn', 'level': 250},
    {'river': 'Shyzhyn River', 'season': 'winter', 'level': 100},
    {'river': 'Shyzhyn River', 'season': 'spring', 'level': 120},
    {'river': 'Shyzhyn River', 'season': 'summer', 'level': 180},
    {'river': 'Shyzhyn River', 'season': 'autumn', 'level': 150}
]

# Визуализация данных о водном уровне на карте
for data in water_level_data:
    folium.Marker(
        location=[centroid.y, centroid.x],
        popup=f"{data['river']} - {data['season']}: {data['level']} м",
        icon=folium.Icon(color='blue' if data['river'] == 'Ili River' else 'red')
    ).add_to(m)

# Сохранение карты
m.save("160.html")