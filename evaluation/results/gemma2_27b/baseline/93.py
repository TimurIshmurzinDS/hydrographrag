import geopandas as gpd
import folium

# Загрузка данных о реках
rivers = gpd.read_file("path/to/rivers.shp")

# Фильтрация по притокам реки Каратал
karatal_tributaries = rivers[rivers["name"].str.contains("Karatal", regex=False)]

# Расчет общей протяженности
total_length = karatal_tributaries["length"].sum()

print(f"Общая протяженность рек-притоков реки Каратал: {total_length} единиц")

# Визуализация (необязательно)
m = folium.Map(location=[43.8, 76.5], zoom_start=8)
folium.GeoJson("path/to/rivers.geojson").add_to(m)
m.save("93.html")