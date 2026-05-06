import geopandas as gpd
from shapely.geometry import LineString
import folium

# Загрузка данных о реках
emel = gpd.read_file('path_to_emel.shp')
karat = gpd.read_file('path_to_karat.shp')

# Проверка наличия пересечения
intersection = emel.intersection(karat)

if not intersection.is_empty:
    # Определение индекса пересекающейся строки в karat
    intersect_index = karat.index[karat.intersects(intersection)].tolist()
    
    if len(intersect_index) > 0:
        # Выбор первой найденной строки (можно изменить на логику выбора конкретной строки)
        intersect_row = karat.iloc[intersect_index[0]]
        
        # Создание LineString из пересекающейся строки
        intersect_line = LineString(intersect_row.geometry.coords)
        
        # Вычисление длины участка
        length_intersect = intersect_line.length
        
        print(f"Длина участка реки Каратал, являющегося притоком реки Емель: {length_intersect} м")
        
        # Визуализация на карте
        m = folium.Map(location=[karat.geometry.centroid.y.mean(), karat.geometry.centroid.x.mean()], zoom_start=10)
        
        folium.GeoJson(emel, name='Reka Emel').add_to(m)
        folium.GeoJson(karat, name='Reka Karat').add_to(m)
        
        # Добавление маркера на точку пересечения
        folium.Marker(intersect_row.geometry.centroid.coords[0], popup=f"Пересечение", icon=folium.Icon(color='red')).add_to(m)
        
        m.save("97.html")
    else:
        print("Не найдено пересекающихся строк.")
else:
    print("Реки Емель и Каратал не пересекаются.")