import geopandas as gpd
import networkx as nx
import folium

# 1. Подготовка данных
data = gpd.read_file("river_network.shp")  # Замените на путь к вашим данным о речной сети

# 2. Определение базовой сети
base_network = data[~data['name'].str.contains('Tentek')]  # Исключаем притоки реки Тентек

# 3. Анализ топологии притоков
tentek_tributaries = data[data['name'].str.contains('Tentek')]
G = nx.from_geopandas(tentek_tributaries)
degree_centrality = nx.degree_centrality(G)

# 4. Создание модели гидрологической сети
# (Этот шаг может варьироваться в зависимости от используемой модели и данных)

# 5. Визуализация результатов
m = folium.Map(location=[data.total_bounds[1], data.total_bounds[0]], zoom_start=8)

folium.GeoJson(data.to_json(), style_function=lambda x, y, z: {'fillColor': 'blue', 'color': 'blue'}).add_to(m)
folium.LayerControl().add_to(m)

m.save("178.html")