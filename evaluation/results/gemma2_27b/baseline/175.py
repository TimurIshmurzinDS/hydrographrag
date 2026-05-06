import geopandas as gpd
import folium

# 1. Загрузка данных
rivers = gpd.read_file("path/to/rivers.shp")

# 2. Расчет коэффициента связности
nodes = rivers.dissolve().explode()
degrees = nodes.geometry.apply(lambda x: len(x.coords))
connectivity = degrees.mean()

print(f"Коэффициент связности речной сети: {connectivity}")

# 3. Визуализация
m = folium.Map(location=[rivers.centroid.y, rivers.centroid.x], zoom_start=10)
folium.GeoJson("path/to/rivers.shp").add_to(m)

# 4. Сохранение карты
m.save("175.html")