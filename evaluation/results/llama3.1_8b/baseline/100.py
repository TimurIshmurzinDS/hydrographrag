import geopandas as gpd
from shapely.geometry import LineString
import folium

# Загрузите данные о реках в формате Shapefile (.shp)
gdf = gpd.read_file('речные_данные.shp')

# Создайте линейную функцию, которая соединяет точки начала и конца каждого участка реки
def create_line(row):
    return LineString([row['geometry'].coords[0], row['geometry'].coords[-1]])

# Примените функцию к каждой строке данных
gdf['line'] = gdf.apply(create_line, axis=1)

# Расчитайте длину каждой линии
gdf['длина'] = gdf['line'].apply(lambda x: x.length)

# Сложите длины всех линий, чтобы получить общую длину речного пути
общая_длина = gdf['длина'].sum()

print(f'Общая длина речного пути: {общая_длина:.2f} метров')

# Создайте карту с маршрутом на реках
m = folium.Map(location=[55.0, 60.0], zoom_start=6)
folium.PolyLine(gdf['geometry'].coords[:].tolist(), color='blue').add_to(m)

# Сохраните карту в файл
m.save("100.html")