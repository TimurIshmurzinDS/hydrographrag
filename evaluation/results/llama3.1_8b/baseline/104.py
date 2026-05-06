import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузите данные о реках в виде геометрических объектов (геометрии)
gdf_shyzyn = gpd.read_file('shyzyn.geojson')
gdf_dos = gpd.read_file('dos.geojson')

# Проверьте, является ли река Шыжын притоком реки Дос
if gdf_dos.geometry.contains(gdf_shyzyn.geometry.any()):
    print("Река Шыжын является притоком реки Дос")
else:
    print("Река Шыжын не является притоком реки Дос")

# Найдите расстояние до их слияния
distance = gdf_dos.geometry.distance(gdf_shyzyn.geometry.any()).min()
print(f"Расстояние до их слияния: {distance} метров")

# Создайте карту с маркерами для обоих рек и линией, соединяющей их слияние
m = folium.Map(location=[gdf_dos.centroid.y.mean(), gdf_dos.centroid.x.mean()], zoom_start=10)
folium.Marker([gdf_shyzyn.geometry.any().y, gdf_shyzyn.geometry.any().x], popup='Река Шыжын').add_to(m)
folium.Marker([gdf_dos.geometry.any().y, gdf_dos.geometry.any().x], popup='Река Дос').add_to(m)

# Нарисуйте линию, соединяющую их слияние
line = folium.PolyLine(list(zip(gdf_shyzyn.geometry.any().coords.xy[0], gdf_shyzyn.geometry.any().coords.xy[1])), color='red')
m.add_child(line)

# Сохраните карту в файл
m.save("104.html")