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

# Пример координат уровней воды для Kurty River и Urzhar River (WKT)
coordinates = [
    {"name": "Kurty River", "wkt": "POINT(76.9345 48.1234)", "level": 10.5},
    {"name": "Urzhar River", "wkt": "POINT(77.0123 48.2345)", "level": 12.3}
]

# Добавление точек уровней воды на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"{coord['name']}: Уровень стока {coord['level']} м",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("108.html")