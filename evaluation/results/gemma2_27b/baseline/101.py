import geopandas as gpd
import folium

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp")

# Определение притоков реки Емель
emel = rivers[rivers["name"] == "Емель"]
tentek = rivers[rivers["name"] == "Тентек"]
byzh = rivers[rivers["name"] == "Быж"]

# Проверка пересечений с рекой Емель
if tenek.intersects(emel).any():
    print("Река Тентек является притоком реки Емель.")
if byzh.intersects(emel).any():
    print("Река Быж является притоком реки Емель.")

# Визуализация на карте
m = folium.Map()
folium.GeoJson(rivers[rivers["name"] == "Емель"], name="Емель").add_to(m)
folium.GeoJson(tentek, name="Тентек", color="blue").add_to(m)
folium.GeoJson(byzh, name="Быж", color="red").add_to(m)

# Сохранение карты
m.save("101.html")