import geopandas as gpd
from shapely.geometry import shape
from folium import Map, Marker

# Загрузите данные о точках слияния рек в формате GeoJSON
gdf = gpd.read_file('points.geojson')

# Создайте слой для каждой точки слияния реки
layer1 = gdf[gdf['name'] == 'Киши-Осек']
layer2 = gdf[gdf['name'] == 'Талгар']

# Вычислите гидрологическое расстояние между точками слияния рек
def distance(point1, point2):
    return point1.distance(point2)

distance_km = layer1.geometry.iloc[0].distance(layer2.geometry.iloc[0]) / 1000

print(f'Гидрологическое расстояние между точками слияния реки Киши-Осек и реки Талгар: {distance_km} км')

# Если необходимо визуализировать результат на карте
m = Map(location=[43.5, 76.5], zoom_start=10)
Marker([layer1.geometry.iloc[0].y, layer1.geometry.iloc[0].x], popup='Киши-Осек').add_to(m)
Marker([layer2.geometry.iloc[0].y, layer2.geometry.iloc[0].x], popup='Талгар').add_to(m)

m.save("171.html")