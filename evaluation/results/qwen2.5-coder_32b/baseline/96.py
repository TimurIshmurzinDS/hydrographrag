import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic
import folium

# Загрузка данных о реках из GeoFabrik (например, для региона Казахстана)
url = "https://download.geofabrik.de/asia/kazakhstan-latest-free.shp.zip"
gdf = gpd.read_file(url)

# Фильтрация данных по типу объектов (рекам)
rivers = gdf[gdf['fclass'] == 'river']

# Поиск рек Уржар и Дос
urzhar_river = rivers[rivers['name'].str.contains('Уржар', na=False)]
dos_river = rivers[rivers['name'].str.contains('Дос', na=False)]

# Определение гидрографических точек (начало и конец) для реки Уржар
if not urzhar_river.empty:
    uz_start_point = Point(urzhar_river.geometry.iloc[0].coords[0])
    uz_end_point = Point(urzhar_river.geometry.iloc[0].coords[-1])

# Определение гидрографических точек (начало и конец) для реки Дос
if not dos_river.empty:
    ds_start_point = Point(dos_river.geometry.iloc[0].coords[0])
    ds_end_point = Point(dos_river.geometry.iloc[0].coords[-1])

# Вычисление расстояния между гидрографическими точками рек Уржар и Дос
if not urzhar_river.empty and not dos_river.empty:
    distance = geodesic((uz_start_point.y, uz_start_point.x), (ds_start_point.y, ds_start_point.x)).kilometers
    print(f"Расстояние между гидрографическими точками рек Уржар и Дос: {distance:.2f} км")

# Визуализация на карте с помощью folium
m = folium.Map(location=[45.0, 71.0], zoom_start=6)

if not urzhar_river.empty:
    folium.PolyLine(urzhar_river.geometry.iloc[0].coords, color='blue').add_to(m)
    folium.Marker([uz_start_point.y, uz_start_point.x], popup='Начало Уржар', icon=folium.Icon(color='blue')).add_to(m)
    folium.Marker([uz_end_point.y, uz_end_point.x], popup='Конец Уржар', icon=folium.Icon(color='blue')).add_to(m)

if not dos_river.empty:
    folium.PolyLine(dos_river.geometry.iloc[0].coords, color='green').add_to(m)
    folium.Marker([ds_start_point.y, ds_start_point.x], popup='Начало Дос', icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([ds_end_point.y, ds_end_point.x], popup='Конец Дос', icon=folium.Icon(color='green')).add_to(m)

# Сохранение карты в файл
m.save("96.html")