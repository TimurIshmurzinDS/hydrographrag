import geopandas as gpd
import folium

# Загрузка данных о реке Шынжалы (замените на актуальный путь к файлу)
river = gpd.read_file("shynzhaly_river.shp")

# Загрузка данных об экологических показателях (замените на актуальный путь к файлу)
eco_data = gpd.read_file("ecological_data.shp")

# Пространственный анализ (пример буферизации)
buffer = river.buffer(1000)  # Создаем буфер 1000 метров вокруг реки

# Объединение данных о реке и экологических показателях
merged_data = gpd.overlay(buffer, eco_data, how='intersection')

# Создание карты с folium
m = folium.Map(location=[river.unary_union.y, river.unary_union.x], zoom_start=12)

# Добавление слоя реки на карту
folium.GeoJson(river).add_to(m)

# Добавление слоя экологических данных на карту
folium.GeoJson(merged_data).add_to(m)

# Сохранение карты
m.save("44.html")