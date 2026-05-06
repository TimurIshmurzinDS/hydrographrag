import geopandas as gpd
import folium

# Загрузка данных о реке Талгар (файл shapefile)
river = gpd.read_file("talgar_river.shp")

# Загрузка данных об экологических показателях (CSV файл)
eco_data = pd.read_csv("eco_data.csv")

# Интерполяция данных об экологических показателях

# Создание модели оценки экологического состояния

# Присвоение значений модели к геометрическим объектам реки

# Создание карты с folium
m = folium.Map(location=[43.25, 76.9], zoom_start=12)

# Добавление слоя реки на карту
folium.GeoJson(river).add_to(m)

# Визуализация результатов моделирования на карте

# Сохранение карты
m.save("32.html")