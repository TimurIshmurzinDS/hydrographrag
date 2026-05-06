import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами наблюдательного пункта
observations = [
    {
        "name": "2 km above mouth of Prokhodnoy River",
        "coordinates": wkt.loads("POINT(37.618423 55.755826)")  # Примерные координаты, заменить на реальные
    }
]

# Добавление маркеров наблюдательных пунктов на карту
for obs in observations:
    folium.Marker(
        location=[obs["coordinates"].y, obs["coordinates"].x],
        popup=obs["name"],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("67.html")