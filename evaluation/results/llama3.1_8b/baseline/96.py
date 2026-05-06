import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузите данные о реках Уржар и Дос из источника данных (например, из базы данных или файла Shapefile)
gdf_urzh = gpd.read_file('urzh.shp')
gdf_dos = gpd.read_file('dos.shp')

# Создайте географические объекты для каждой реки
geometry_urzh = gdf_urzh.geometry.iloc[0]
geometry_dos = gdf_dos.geometry.iloc[0]

# Определите гидрографические точки для каждой реки (например, конечные точки реки)
hydro_point_urzh = geometry_urzh.coords[-1]
hydro_point_dos = geometry_dos.coords[-1]

# Рассчитайте расстояние между гидрографическими точками двух рек
distance = ((hydro_point_urzh[0] - hydro_point_dos[0]) ** 2 + (hydro_point_urzh[1] - hydro_point_dos[1]) ** 2) ** 0.5

# Визуализируйте результаты на карте с помощью библиотеки folium
m = folium.Map(location=[55, 60], zoom_start=6)
folium.Marker([hydro_point_urzh[1], hydro_point_urzh[0]], popup='Река Уржар').add_to(m)
folium.Marker([hydro_point_dos[1], hydro_point_dos[0]], popup='Река Дос').add_to(m)

# Сохраните карту в файл
m.save("96.html")

print(f"Расстояние между реками Уржар и Дос: {distance} км")