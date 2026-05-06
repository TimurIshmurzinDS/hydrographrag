import osmnx as ox
import networkx as nx
import folium
from shapely.geometry import LineString, Point

def analyze_talgar_basin():
    # 1. Определение области интереса (район реки Талгар, Казахстан)
    # Используем поиск по названию или координаты центра бассейна
    place_name = "Talgar, Kazakhstan"
    
    print(f"Загрузка данных речной сети для региона: {place_name}...")
    # Загружаем все водные пути в радиусе 30 км от центра Талгара
    # В реальном проекте здесь используется полигон бассейна
    gdf = ox.features_from_place(place_name, tags={"waterway": True})
    
    # Оставляем только линейные объекты
    rivers = gdf[gdf.geometry.type == 'LineString']
    
    if rivers.empty:
        print("Данные о реках не найдены. Попробуем расширить область поиска.")
        # Запасной вариант: поиск по более широкому тегу или области
        return

    # 2. Построение графа речной сети
    G = nx.DiGraph()
    
    for idx, row in rivers.iterrows():
        coords = list(row.geometry.coords)
        # Добавляем ребра между последовательными точками линии
        for i in range(len(coords) - 1):
            u = coords[i]
            v = coords[i+1]
            G.add_edge(u, v, weight=Point(u).distance(Point(v)))

    # 3. Поиск узлов слияния
    # Узел слияния - это точка, где сходятся несколько притоков
    confluence_nodes = []
    for node in G.nodes():
        # Входящие ребра (притоки) и исходящие (основное русло)
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        
        # Критерий слияния: минимум 2 входящих потока и 1 исходящий
        if in_degree >= 2 and out_degree >= 1:
            confluence_nodes.append(node)

    print(f"Обнаружено основных узлов слияния: {len(confluence_nodes)}")

    # 4. Визуализация с помощью folium
    # Центрируем карту по первой найденной реке
    centroid = rivers.geometry.centroid.iloc[0]
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=11, tiles="CartoDB positron")

    # Рисуем все реки
    for _, row in rivers.iterrows():
        coords = [[p[1], p[0]] for p in row.geometry.coords]
        folium.PolyLine(coords, color="blue", weight=2, opacity=0.7).add_to(m)

    # Рисуем узлы слияния
    for node in confluence_nodes:
        folium.CircleMarker(
            location=[node[1], node[0]],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            popup="Узел слияния притоков"
        ).add_to(m)

    # Сохранение результата
    m.save("166.html")
    print("Анализ завершен. Карта сохранена в файл 166.html")

if __name__ == "__main__":
    # Настройка osmnx для корректной работы с геометриями
    ox.settings.use_cache = True
    try:
        analyze_talgar_basin()
    except Exception as e:
        print(f"Произошла ошибка при выполнении моделирования: {e}")