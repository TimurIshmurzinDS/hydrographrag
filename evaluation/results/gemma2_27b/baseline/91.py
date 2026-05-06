import geopandas as gpd
import folium

# Загрузить данные о речной сети
rivers = gpd.read_file("path/to/river_network.shp")

# Найти ID реки Уржар (заменить на ID из ваших данных)
urzar_id = rivers[rivers["name"] == "Уржар"].index[0]

# Найти все притоки реки Уржар
tributaries = rivers[rivers["downstream"] == urzar_id]

# Извлечь координаты притоков
coordinates = tributaries.geometry.apply(lambda x: [x.coords[0], x.coords[-1]])

# Создать карту Folium
m = folium.Map(location=[coordinates.iloc[0][0][1], coordinates.iloc[0][0][0]], zoom_start=12)

# Добавить притоки на карту
for i, coord in enumerate(coordinates):
    folium.PolyLine(locations=coord, color="blue", opacity=0.5).add_to(m)

# Сохранить карту
m.save("91.html")