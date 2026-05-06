import geopandas as gpd
import networkx as nx
import folium

# Загрузка данных о речной сети
rivers = gpd.read_file("rivers.shp")

# Определение координат истока реки Шынжалы
source_coords = (43.25, 76.80)  # Примерные координаты

# Создание графа из данных о речной сети
G = nx.from_pandas_edgelist(rivers, source="source", target="target")

# Трейсинг стока от источника реки Шынжалы
path = nx.shortest_path(G, source=source_coords)

# Создание карты Folium
m = folium.Map()

# Добавление слоя речной сети на карту
folium.GeoJson("rivers.geojson").add_to(m)

# Добавление линии трейсинга стока на карту
folium.PolyLine(path, color="red", opacity=0.5).add_to(m)

# Сохранение карты
m.save("173.html")