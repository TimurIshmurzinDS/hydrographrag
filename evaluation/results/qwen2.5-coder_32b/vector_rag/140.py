import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат датчиков (WKT) для рек Токыраун и Аягоз
sensors = [
    {"name": "Tokyraun_Sensor_1", "coordinates": wkt.loads("POINT(76.93 42.85)"), "status": "active"},
    {"name": "Tokyraun_Sensor_2", "coordinates": wkt.loads("POINT(76.94 42.86)"), "status": "inactive"},
    {"name": "Ayagoz_Sensor_1", "coordinates": wkt.loads("POINT(77.00 43.00)"), "status": "active"}
]

# Добавление маркеров датчиков на карту
for sensor in sensors:
    folium.Marker(
        location=[sensor["coordinates"].y, sensor["coordinates"].x],
        popup=f"{sensor['name']} - {sensor['status']}",
        icon=folium.Icon(color='green' if sensor['status'] == 'active' else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("140.html")