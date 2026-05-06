import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водной системе из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о гидропостах (координаты и уровни воды)
hydro_stations = [
    {"name": "ГП1", "coordinates": wkt.loads("POINT(49.8333 56.1667)"), "water_level_cm": 120, "date": "2023-10-01"},
    {"name": "ГП2", "coordinates": wkt.loads("POINT(49.8500 56.1833)"), "water_level_cm": 130, "date": "2023-10-01"},
    {"name": "ГП3", "coordinates": wkt.loads("POINT(49.8750 56.2000)"), "water_level_cm": 115, "date": "2023-10-01"}
]

# Добавление гидропостов на карту
for station in hydro_stations:
    folium.Marker(
        location=[station["coordinates"].y, station["coordinates"].x],
        popup=f"ГП: {station['name']}\nУровень воды: {station['water_level_cm']} см\nДата измерения: {station['date']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("63.html")