import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о гидропостах (координаты и наблюдения)
hydro_stations = [
    {"name": "Station_1", "coordinates": wkt.loads("POINT(37.5 56.0)"), "Water_consumption_Value": [100, 120, 150, 200, 250]},
    {"name": "Station_2", "coordinates": wkt.loads("POINT(38.0 56.5)"), "Water_consumption_Value": [110, 130, 140, 170, 220]},
    {"name": "Station_3", "coordinates": wkt.loads("POINT(37.8 56.3)"), "Water_consumption_Value": [90, 110, 130, 160, 210]}
]

# Проверка на резкие росты расхода воды
def has_sudden_increase(values):
    for i in range(1, len(values)):
        if values[i] > values[i-1] * 1.5:  # Примерный порог для резкого роста
            return True
    return False

# Добавление гидропостов на карту и выделение тех с резкими ростами расхода воды
for station in hydro_stations:
    coordinates = (station["coordinates"].y, station["coordinates"].x)
    if has_sudden_increase(station["Water_consumption_Value"]):
        folium.Marker(coordinates, popup=f"{station['name']} - Резкий рост", icon=folium.Icon(color='red')).add_to(m)
    else:
        folium.Marker(coordinates, popup=station['name']).add_to(m)

# Сохранение карты
m.save("84.html")