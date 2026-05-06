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

# Пример данных о уровне воды (WKT координаты точки измерения)
water_level_data = [
    {"coordinates": "POINT(37.618421 55.755826)", "level_cm": 150, "date": "2023-09-15"},
    {"coordinates": "POINT(37.619421 55.756826)", "level_cm": 160, "date": "2023-09-16"}
]

# Добавление точек измерения уровня воды на карту
for data in water_level_data:
    point = wkt.loads(data["coordinates"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Уровень воды: {data['level_cm']} см\nДата: {data['date']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("233.html")