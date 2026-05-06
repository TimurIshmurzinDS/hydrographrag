import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Батарейка
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Батарейка
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат наблюдений (WKT), если они доступны
observations = [
    {"coordinates": "POINT(37.618421 55.755826)", "water_level": 150, "date": "2023-10-01"},
    {"coordinates": "POINT(37.619421 55.756826)", "water_level": 152, "date": "2023-10-02"}
]

# Добавление маркеров наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["coordinates"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Уровень воды: {obs['water_level']} м\nДата: {obs['date']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("14.html")