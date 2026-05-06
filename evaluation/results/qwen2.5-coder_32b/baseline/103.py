import geopandas as gpd
from shapely.geometry import LineString
import folium

# Шаг 1: Загрузка данных о реках из GeoJSON файла (пример)
# Предположим, что у нас есть GeoJSON файл с данными о реках
gdf = gpd.read_file('rivers.geojson')

# Шаг 2: Фильтрация данных для нужных рек
selected_rivers = ['Уржар', 'Дос', 'Каратал']
filtered_gdf = gdf[gdf['name'].isin(selected_rivers)]

# Шаг 3: Извлечение координат и вывод их на экран
coordinates_dict = {}
for idx, row in filtered_gdf.iterrows():
    river_name = row['name']
    coordinates = list(row.geometry.coords)
    coordinates_dict[river_name] = coordinates
    print(f"Координаты реки {river_name}:")
    for coord in coordinates:
        print(coord)

# Шаг 4: Визуализация на карте с помощью folium
m = folium.Map(location=[50.2647, 83.2220], zoom_start=10)  # Координаты примерного центра региона

for idx, row in filtered_gdf.iterrows():
    river_name = row['name']
    coordinates = list(row.geometry.coords)
    folium.PolyLine(coordinates, color='blue', weight=2.5, opacity=1).add_to(m)
    folium.Marker(coordinates[0], popup=f"Начало реки {river_name}").add_to(m)
    folium.Marker(coordinates[-1], popup=f"Конец реки {river_name}").add_to(m)

# Шаг 5: Сохранение карты в файл HTML
m.save("103.html")