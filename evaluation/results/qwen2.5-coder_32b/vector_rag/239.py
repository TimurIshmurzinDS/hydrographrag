import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат наблюдения (WKT)
observations = [
    {"name": "Observation_1", "wkt": "POINT(39.876543 40.123456)", "water_level": 150, "date": "2023-10-01"},
    {"name": "Observation_2", "wkt": "POINT(39.876543 40.123456)", "water_level": 160, "date": "2023-10-02"}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Наблюдение: {obs['name']}<br>Уровень воды: {obs['water_level']} см<br>Дата: {obs['date']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("239.html")