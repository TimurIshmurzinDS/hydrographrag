import geopandas as gpd
import folium

# Загрузка данных о реке и садах
river = gpd.read_file("river_data.shp")
gardens = gpd.read_file("gardens.shp")

# Расчет расстояния от садов до реки
distances = gpd.sjoin(gardens, river, how="left", op="nearest").distance

# Корреляция с состоянием стока (необходимо добавить код для анализа)

# Создание карты
m = folium.Map(location=[river.centroid.y, river.centroid.x], zoom_start=10)

# Добавление слоя реки на карту
folium.GeoJson("river_data.shp").add_to(m)

# Добавление слоя садов на карту
gardens["distance"] = distances
folium.GeoJson(gardens, name="Gardens", tooltip=folium.GeoJsonTooltip(fields=["distance"])).add_to(m)

# Сохранение карты
m.save("183.html")