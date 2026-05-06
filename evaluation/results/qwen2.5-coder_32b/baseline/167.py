import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
import folium

# Шаг 1: Загрузка данных (предположим, что у нас есть файл GeoJSON с речными сетями)
rivers_gdf = gpd.read_file('path_to_your_river_network.geojson')

# Шаг 2: Фильтрация данных для получения только рек Текес и Тентек
tekes = rivers_gdf[rivers_gdf['name'] == 'Текес']
tenteck = rivers_gdf[rivers_gdf['name'] == 'Тентек']

# Предположим, что у нас есть функция для поиска речной сети между двумя точками
def find_river_network_between_points(rivers_gdf, start_point, end_point):
    # Здесь должен быть реализован алгоритм поиска пути в графе речных сетей.
    # Для простоты предположим, что мы уже знаем, какие участки речной сети нас интересуют.
    # В реальном случае это может потребовать использования алгоритма поиска кратчайшего пути (например, Dijkstra).
    
    # Пример: выбираем все линии из GeoDataFrame
    selected_rivers = rivers_gdf[(rivers_gdf['name'] == 'Текес') | (rivers_gdf['name'] == 'Тентек')]
    
    return selected_rivers

# Шаг 3: Идентификация речных сетей между рекой Текес и рекой Тентек
start_point = tekes.geometry.iloc[0].coords[0]  # Начальная точка (например, начало реки Текес)
end_point = tenteck.geometry.iloc[0].coords[0]    # Конечная точка (например, начало реки Тентек)

selected_rivers = find_river_network_between_points(rivers_gdf, start_point, end_point)

# Шаг 4: Расчет протяженности речной сети
total_length = selected_rivers.geometry.length.sum()
print(f"Общая протяженность речной сети: {total_length} метров")

# Шаг 5: Визуализация на карте с использованием folium
m = folium.Map(location=[42.8746, 79.1743], zoom_start=10)  # Координаты примерно по центру региона

# Добавление рек Текес и Тентек на карту
for _, row in selected_rivers.iterrows():
    folium.PolyLine(locations=row.geometry.coords, color='blue', weight=2.5).add_to(m)

# Сохранение карты в файл
m.save("167.html")