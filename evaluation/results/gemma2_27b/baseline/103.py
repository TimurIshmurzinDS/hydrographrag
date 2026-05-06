import geopandas as gpd
import folium

# Загрузка данных о реках
rivers = gpd.read_file("path/to/rivers.shp")

# Фильтрация данных по названию реки
urzar = rivers[rivers["name"] == "Urzar"]
dos = rivers[rivers["name"] == "Dos"]
karatal = rivers[rivers["name"] == "Karatal"]

# Извлечение координат рек
urzar_coords = list(zip(urzar.geometry.x, urzar.geometry.y))
dos_coords = list(zip(dos.geometry.x, dos.geometry.y))
karatal_coords = list(zip(karatal.geometry.x, karatal.geometry.y))

# Вывод координат
print("Координаты реки Уржар:", urzar_coords)
print("Координаты реки Дос:", dos_coords)
print("Координаты реки Каратал:", karatal_coords)

# Визуализация на карте (необязательно)
m = folium.Map()
folium.GeoJson(urzar).add_to(m)
folium.GeoJson(dos).add_to(m)
folium.GeoJson(karatal).add_to(m)

m.save("103.html")