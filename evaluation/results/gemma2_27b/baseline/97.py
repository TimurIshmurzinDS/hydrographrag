import geopandas as gpd
from shapely.geometry import Point
from geopy.distance import geodesic

# Загрузка данных о реках
rivers = gpd.read_file("rivers.shp")

# Выбор данных о реках Емель и Каратал
emel = rivers[rivers["name"] == "Емель"]
karatal = rivers[rivers["name"] == "Каратал"]

# Поиск точки пересечения рек
intersection = gpd.overlay(emel, karatal, how="intersection")

# Проверка наличия точки пересечения
if not intersection.empty:
    print("Река Емель является притоком реки Каратал.")

    # Получение координат точки пересечения
    intersection_point = Point(intersection.geometry.x[0], 
                              intersection.geometry.y[0])

    # Расчет длины участка реки Емель
    length = geodesic(intersection_point, emel.geometry.iloc[-1]).km

    print("Длина участка реки Емель:", length, "км")

else:
    print("Река Емель не является притоком реки Каратал.")