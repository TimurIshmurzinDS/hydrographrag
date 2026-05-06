import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о реках Уржар и Дос
urzhar = gpd.read_file('path_to_urzhar_shapefile.shp')
dos = gpd.read_file('path_to_dos_shapefile.shp')

# Определение гидрографических точек (например, узлов)
urzhar_nodes = urzhar[urzhar['geometry'].type == 'Point']
dos_nodes = dos[dos['geometry'].type == 'Point']

# Вычисление расстояния между точками
if not urzhar_nodes.empty and not dos_nodes.empty:
    min_distance = float('inf')
    closest_points = None
    
    for point1 in urzhar_nodes.geometry:
        for point2 in dos_nodes.geometry:
            distance = point1.distance(point2)
            if distance < min_distance:
                min_distance = distance
                closest_points = (point1, point2)
    
    print(f"Минимальное расстояние между гидрографическими точками: {min_distance} м")
else:
    print("Не найдено гидрографических точек для одной или обеих рек.")

# Визуализация на карте
m = folium.Map(location=[urzhar.geometry.centroid.y.mean(), urzhar.geometry.centroid.x.mean()], zoom_start=10)

folium.GeoJson(urzhar, name='Urzhar').add_to(m)
folium.GeoJson(dos, name='Dos').add_to(m)

if closest_points:
    folium.Marker(list(closest_points[0].coords)[0], popup='Точка Уржар', icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(list(closest_points[1].coords)[0], popup='Точка Дос', icon=folium.Icon(color='blue')).add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("96.html")