import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат для уровня воды (WKT)
coordinates = [
    {"name": "Kurty River", "date": "2023-10-01", "level": 50, "wkt": "POINT(48.765 42.987)"},
    {"name": "Kurty River", "date": "2023-10-02", "level": 52, "wkt": "POINT(48.765 42.987)"},
    {"name": "Dos River", "date": "2023-10-01", "level": 45, "wkt": "POINT(48.760 42.990)"},
    {"name": "Dos River", "date": "2023-10-02", "level": 47, "wkt": "POINT(48.760 42.990)"}
]

# Добавление маркеров на карту
for coord in coordinates:
    point = wkt.loads(coord['wkt'])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"{coord['name']} - {coord['date']}: Уровень воды {coord['level']} м",
        icon=folium.Icon(color='blue' if coord['name'] == 'Kurty River' else 'red')
    ).add_to(m)

# Сохранение карты
m.save("133.html")