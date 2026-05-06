import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассина (только для контекста)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассина на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты точки наблюдения (пример, нужно заменить реальными координатами)
observation_point = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [37.123456, 40.987654]  # Примерные координаты
    },
    "properties": {
        "name": "0.2 km above the confluence with Osek River"
    }
}

# Добавление точки наблюдения на карту
folium.Marker(
    location=[observation_point['geometry']['coordinates'][1], observation_point['geometry']['coordinates'][0]],
    popup=observation_point['properties']['name'],
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# Сохранение карты
m.save("267.html")