import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат точек интереса (WKT) для рек Kurty River, Urzhar River и Byzhy River
points_wkt = [
    {"name": "Kurty River", "wkt": "POINT(48.123 50.456)"},
    {"name": "Urzhar River", "wkt": "POINT(48.789 50.123)"},
    {"name": "Byzhy River", "wkt": "POINT(48.456 50.789)"}
]

# Преобразование WKT в точки и добавление на карту
for point in points_wkt:
    geom = wkt.loads(point['wkt'])
    folium.Marker([geom.y, geom.x], popup=point['name']).add_to(m)

# Сохранение карты в HTML файл
m.save("112.html")