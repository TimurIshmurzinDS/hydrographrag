import osmnx as ox
import folium
import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString, Point

def analyze_river_network():
    # 1. Определение области поиска (регион, где протекают реки Текес и Сарыкан)
    # Для примера используем поиск по ключевым словам в регионе
    place_name = "Zhetysu Region, Kazakhstan"
    
    print("Загрузка гидрографических данных из OSM...")
    # Загружаем все объекты типа 'waterway'
    gdf = ox.features_from_place(place_name, tags={'waterway': True})

    # 2. Фильтрация рек Текес и Сарыкан
    # Приводим названия к нижнему регистру для надежности поиска
    rivers_of_interest = ['текес', 'сарыкан']
    
    # Создаем маску для фильтрации
    mask = gdf['name'].fillna('').str.lower().apply(
        lambda x: any(river in x for river in rivers_of_interest)
    )
    river_network = gdf[mask].copy()

    if river_network.empty:
        print("Реки не найдены в данной области. Попробуйте расширить область поиска.")
        return

    # 3. Анализ конфигурации
    # Выделяем каждую реку отдельно для анализа их взаимодействия
    tekes = river_network[river_network['name'].fillna('').str.lower().str.contains('текес')]
    sarykan = river_network[river_network['name'].fillna('').str.lower().str.contains('сарыкан')]

    # Поиск точки слияния (упрощенно: поиск ближайших точек между двумя геометриями)
    # В реальности реки могут быть представлены множеством сегментов
    confluence_point = None
    min_dist = float('inf')
    
    for geom_t in tekes.geometry:
        for geom_s in sarykan.geometry:
            dist = geom_t.distance(geom_s)
            if dist < min_dist:
                min_dist = dist
                # Берем среднюю точку между ближайшими точками
                confluence_point = Point((geom_t.centroid.x + geom_s.centroid.x)/2, 
                                        (geom_t.centroid.y + geom_s.centroid.y)/2)

    # 4. Визуализация с помощью folium
    # Центрируем карту по одной из рек
    center_lat = tekes.geometry.centroid.y.mean()
    center_lon = tekes.geometry.centroid.x.mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='CartoDB positron')

    # Добавление рек на карту
    for _, row in tekes.iterrows():
        if row.geometry.geom_type == 'LineString':
            coords = [[p[1], p[0]] for p in row.geometry.coords]
            folium.PolyLine(coords, color='blue', weight=4, opacity=0.8, tooltip='Река Текес').add_to(m)
        elif row.geometry.geom_type == 'MultiLineString':
            for line in row.geometry.geoms:
                coords = [[p[1], p[0]] for p in line.coords]
                folium.PolyLine(coords, color='blue', weight=4, opacity=0.8, tooltip='Река Текес').add_to(m)

    for _, row in sarykan.iterrows():
        if row.geometry.geom_type == 'LineString':
            coords = [[p[1], p[0]] for p in row.geometry.coords]
            folium.PolyLine(coords, color='green', weight=4, opacity=0.8, tooltip='Река Сарыкан').add_to(m)
        elif row.geometry.geom_type == 'MultiLineString':
            for line in row.geometry.geoms:
                coords = [[p[1], p[0]] for p in line.coords]
                folium.PolyLine(coords, color='green', weight=4, opacity=0.8, tooltip='Река Сарыкан').add_to(m)

    # Отметка точки слияния
    if confluence_point:
        folium.Marker(
            location=[confluence_point.y, confluence_point.x],
            popup='Предполагаемая точка слияния/связи',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    # Сохранение карты
    m.save("180.html")
    print("Анализ завершен. Карта сохранена в файл 180.html")

if __name__ == "__main__":
    analyze_river_network()