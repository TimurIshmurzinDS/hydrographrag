import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о реках
shyzyn_gdf = gpd.read_file('path_to_shyzyn.shp')
dos_gdf = gpd.read_file('path_to_dos.shp')

# Проверка, является ли Шыжын притоком Дос
def is_inflow(shyzyn, dos):
    # Простой метод: проверяем, находится ли точка начала Шыжын внутри полигона Дос
    return shyzyn.geometry.within(dos.geometry)

# Найдем точки начала и конца для каждой реки
shyzyn_start = Point(shyzyn_gdf.iloc[0].geometry.x, shyzyn_gdf.iloc[0].geometry.y)
dos_end = Point(dos_gdf.iloc[-1].geometry.x, dos_gdf.iloc[-1].geometry.y)

# Проверка, является ли Шыжын притоком Дос
is_inflow_result = is_inflow(shyzyn_start, dos_gdf)

if is_inflow_result:
    # Найдем точку слияния (простой метод: ближайшая точка на конечном участке Дос)
    min_distance = float('inf')
    merge_point = None
    for point in shyzyn_gdf.geometry:
        distance = dos_end.distance(point)
        if distance < min_distance:
            min_distance = distance
            merge_point = point
    
    # Создание карты для визуализации
    m = folium.Map(location=[(shyzyn_start.y + dos_end.y) / 2, (shyzyn_start.x + dos_end.x) / 2], zoom_start=10)
    
    # Добавление линий на карту
    folium.GeoJson(shyzyn_gdf).add_to(m)
    folium.GeoJson(dos_gdf).add_to(m)
    
    # Добавление точек начала и конца
    folium.Marker([shyzyn_start.y, shyzyn_start.x], popup='Начало Шыжын', icon=folium.Icon(color='red')).add_to(m)
    folium.Marker([dos_end.y, dos_end.x], popup='Конец Дос', icon=folium.Icon(color='blue')).add_to(m)
    
    # Добавление точки слияния
    if merge_point:
        folium.Marker([merge_point.y, merge_point.x], popup=f'Точка слияния (расстояние: {min_distance:.2f} м)', icon=folium.Icon(color='green')).add_to(m)
    
    # Сохранение карты
    m.save("104.html")
else:
    print("Шыжын не является притоком Дос")

print(f"Расстояние до слияния: {min_distance:.2f} м") if is_inflow_result else None