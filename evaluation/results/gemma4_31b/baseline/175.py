import geopandas as gpd
import networkx as nx
import folium
from shapely.geometry import LineString, Point

def calculate_river_connectivity():
    # 1. Создание синтетических данных для реки Сарыкан и её притоков
    # В реальном сценарии здесь будет загрузка файла: gdf = gpd.read_file("sarykan_network.shp")
    # Координаты представлены схематично (Широта, Долгота)
    data = {
        'river_name': ['Sarykan_Main', 'Tributary_1', 'Tributary_2', 'Tributary_3', 'Sarykan_Lower'],
        'geometry': [
            LineString([(70.1, 45.1), (70.2, 45.2)]), # Main segment 1
            LineString([(70.0, 45.0), (70.1, 45.1)]), # Tributary 1 -> Main 1
            LineString([(70.3, 45.1), (70.2, 45.2)]), # Tributary 2 -> Main 1
            LineString([(70.2, 45.3), (70.2, 45.2)]), # Tributary 3 -> Main 1
            LineString([(70.2, 45.2), (70.4, 45.3)]), # Main segment 2 (Lower)
        ]
    }
    gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

    # 2. Построение графа связности
    G = nx.Graph()
    
    for idx, row in gdf.iterrows():
        coords = list(row['geometry'].coords)
        start_node = coords[0]
        end_node = coords[-1]
        # Добавляем ребро между начальной и конечной точкой сегмента
        G.add_edge(start_node, end_node, weight=row['geometry'].length)

    # 3. Расчет коэффициента связности
    num_edges = G.number_of_edges()
    num_nodes = G.number_of_nodes()
    connectivity_coeff = num_edges / num_nodes if num_nodes > 0 else 0

    print(f"Количество узлов (V): {num_nodes}")
    print(f"Количество ребер (E): {num_edges}")
    print(f"Коэффициент связности (beta = E/V): {connectivity_coeff:.4f}")

    # 4. Визуализация с помощью folium
    # Центрируем карту по средним координатам
    center_lat = 45.2
    center_lon = 70.2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8, tiles='CartoDB positron')

    # Добавление рек на карту
    for idx, row in gdf.iterrows():
        # Folium использует [lat, lon], а Shapely часто [lon, lat] 
        # В нашем синтетическом примере мы используем (lat, lon) для простоты
        points = [[p[0], p[1]] for p in row['geometry'].coords]
        folium.PolyLine(points, color="blue", weight=3, opacity=0.8, 
                       tooltip=row['river_name']).add_to(m)

    # Добавление узлов (точек слияния/истоков)
    for node in G.nodes():
        folium.CircleMarker(
            location=[node[0], node[1]],
            radius=3,
            color="red",
            fill=True,
            fill_color="red",
            popup=f"Node: {node}"
        ).add_to(m)

    # Сохранение карты
    m.save("175.html")
    print("Карта сохранена в файл 175.html")

if __name__ == "__main__":
    calculate_river_connectivity()