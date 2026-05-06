import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты folium с центром по центроиду бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о расходе воды (WKT координаты не предоставлены, используем фиксированные данные)
data = [
    {"river": "Kurty River", "year": 2018, "value": 50.0},
    {"river": "Kurty River", "year": 2019, "value": 55.0},
    {"river": "Kurty River", "year": 2020, "value": 60.0},
    {"river": "Kurty River", "year": 2021, "value": 65.0},
    {"river": "Kurty River", "year": 2022, "value": 70.0},
    {"river": "Tekes River", "year": 2018, "value": 150.0},
    {"river": "Tekes River", "year": 2019, "value": 160.0},
    {"river": "Tekes River", "year": 2020, "value": 170.0},
    {"river": "Tekes River", "year": 2021, "value": 180.0},
    {"river": "Tekes River", "year": 2022, "value": 190.0}
]

# Добавление маркеров на карту для каждого года и значения расхода воды
for item in data:
    folium.Marker(
        location=[centroid.y, centroid.x], 
        popup=f"Река: {item['river']}, Год: {item['year']}, Расход воды: {item['value']} м³/с",
        icon=folium.Icon(color='blue' if item['river'] == 'Kurty River' else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("129.html")