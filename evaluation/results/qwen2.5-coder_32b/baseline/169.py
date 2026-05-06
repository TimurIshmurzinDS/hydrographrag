import geopandas as gpd
from shapely.geometry import LineString, Point
import folium

# Шаг 1: Загрузка данных (предположим, что у нас есть файлы 'shynzhal.json' и 'talgat.json')
gdf_shynzhal = gpd.read_file('shynzhal.json')
gdf_talgat = gpd.read_file('talgat.json')

# Шаг 2: Преобразование данных в формат GeoDataFrame
# Предположим, что данные уже находятся в правильном формате

# Шаг 3: Выполнение операции пересечения
intersection = gdf_shynzhal.intersection(gdf_talgat)

# Фильтрация пустых значений (если они есть)
intersection = intersection[~intersection.is_empty]

# Создание GeoDataFrame для результатов пересечения
gdf_intersection = gpd.GeoDataFrame(geometry=intersection, crs=gdf_shynzhal.crs)

# Шаг 4: Визуализация результатов на карте с помощью folium

# Определение центра карты (например, среднее значение координат)
center_lat = (gdf_shynzhal.total_bounds[1] + gdf_shynzhal.total_bounds[3]) / 2
center_lon = (gdf_shynzhal.total_bounds[0] + gdf_shynzhal.total_bounds[2]) / 2

# Создание карты folium
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Добавление русла реки Шынжалы на карту
folium.GeoJson(gdf_shynzhal.to_json(), name='Река Шынжалы').add_to(m)

# Добавление русла реки Талгар на карту
folium.GeoJson(gdf_talgat.to_json(), name='Река Талгар').add_to(m)

# Добавление результатов пересечения на карту
if not gdf_intersection.empty:
    folium.GeoJson(gdf_intersection.to_json(), name='Пересечение', style_function=lambda x: {'color': 'red'}).add_to(m)

# Добавление слоев управления
folium.LayerControl().add_to(m)

# Сохранение карты в HTML-файл
m.save("169.html")