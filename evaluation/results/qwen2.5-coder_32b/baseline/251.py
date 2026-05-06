import geopandas as gpd
import folium

# Шаг 1: Загрузка данных о реке Кумбель из GeoJSON файла
gdf = gpd.read_file('kumbe_river.geojson')

# Шаг 2: Обработка данных (в данном случае, предположим, что данные уже в нужном формате)
# Если необходимо, можно выполнить дополнительные операции по очистке и преобразованию данных

# Шаг 3: Создание карты с использованием folium
m = folium.Map(location=[gdf.centroid.y.mean(), gdf.centroid.x.mean()], zoom_start=10)

# Добавление линий реки на карту
for _, row in gdf.iterrows():
    points = list(zip(row.geometry.xy[1], row.geometry.xy[0]))
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

# Шаг 4: Сохранение карты в HTML файл
m.save("251.html")

print("Карта сохранена как 251.html")