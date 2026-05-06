import folium
import networkx as nx
from shapely.geometry import LineString, Point
import geopandas as gpd

def solve_river_connectivity():
    # 1. Симуляция геоданных (Координаты для реки Эмель и Сарыкан)
    # В реальном проекте здесь будет загрузка shape-файла: gpd.read_file("rivers.shp")
    
    # Основное русло реки Эмель (упрощенно)
    emel_coords = [
        (45.5, 78.0), (45.2, 78.5), (44.8, 79.0), (44.5, 79.5), (44.0, 80.0)
    ]
    
    # Приток Сарыкан (впадает в Эмель в точке 45.2, 78.5)
    sarykan_coords = [
        (45.8, 77.5), (45.6, 77.8), (45.2, 78.5)
    ]
    
    # Создаем LineString объекты
    emel_line = LineString(emel_coords)
    sarykan_line = LineString(sarykan_coords)
    
    # Создаем GeoDataFrame
    rivers_data = {
        'name': ['Emel', 'Sarykan'],
        'geometry': [emel_line, sarykan_line]
    }
    gdf = gpd.GeoDataFrame(rivers_data, crs="EPSG:4326")

    # 2. Построение топологического графа
    G = nx.DiGraph()
    
    # Добавляем ребра для Сарыкана (от истока к устью)
    for i in range(len(sarykan_coords) - 1):
        G.add_edge(sarykan_coords[i], sarykan_coords[i+1], weight=sarykan_line.length / (len(sarykan_coords)-1))
        
    # Добавляем ребра для Эмеля (от точки слияния вниз по течению)
    for i in range(len(emel_coords) - 1):
        G.add_edge(emel_coords[i], emel_coords[i+1], weight=emel_line.length / (len(emel_coords)-1))

    # 3. Оценка связности
    source_sarykan = sarykan_coords[0]
    mouth_emel = emel_coords[-1]
    
    # Проверка: есть ли путь от истока Сарыкана до устья Эмеля
    is_connected = nx.has_path(G, source_sarykan, mouth_emel)
    
    if is_connected:
        path = nx.shortest_path(G, source_sarykan, mouth_emel)
        connectivity_status = f"Связность подтверждена. Путь состоит из {len(path)-1} сегментов."
    else:
        connectivity_status = "Связность отсутствует."

    print(f"Результат анализа: {connectivity_status}")

    # 4. Визуализация с помощью folium
    # Центрируем карту на среднем значении координат
    m = folium.Map(location=[44.8, 78.5], zoom_start=6, tiles='CartoDB positron')

    # Рисуем реку Эмель (Синий цвет)
    folium.PolyLine(emel_coords, color='blue', weight=4, opacity=0.8, 
                    tooltip='Река Эмель (Основное русло)').add_to(m)
    
    # Рисуем реку Сарыкан (Голубой цвет)
    folium.PolyLine(sarykan_coords, color='skyblue', weight=3, opacity=0.8, 
                    tooltip='Река Сарыкан (Приток)').add_to(m)

    # Отмечаем истоки и устья
    folium.Marker(location=source_sarykan, popup='Исток Сарыкана', 
                  icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(location=mouth_emel, popup='Устье Эмеля', 
                  icon=folium.Icon(color='red')).add_to(m)
    
    # Точка слияния
    junction = (45.2, 78.5)
    folium.CircleMarker(location=junction, radius=5, color='purple', 
                       fill=True, popup='Точка слияния Сарыкан -> Эмель').add_to(m)

    # Сохранение карты
    m.save("168.html")
    print("Карта сохранена в файл 168.html")

if __name__ == "__main__":
    solve_river_connectivity()