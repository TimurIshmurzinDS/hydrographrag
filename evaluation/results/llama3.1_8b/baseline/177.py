import geopandas as gpd
from shapely.geometry import shape
from folium import Map, Polygon

# Загрузите данные о границах бассейнов рек из соответствующих источников.
# Для примера мы будем использовать геоданные в формате GeoJSON.

sarikan_basin = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [[-122.0, 37.0], [-121.5, 36.8], [-121.2, 37.1], [-121.9, 37.3],
             [-122.0, 37.0]]
        ]
    },
    "properties": {"name": "Сарыкан"}
}

emel_basin = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [[-123.5, 36.2], [-123.1, 36.4], [-122.8, 36.6],
             [-123.5, 36.2]]
        ]
    },
    "properties": {"name": "Эмель"}
}

# Создайте геодатафреймы для каждого бассейна.
sarikan_gdf = gpd.GeoDataFrame.from_features([sarikan_basin])
emel_gdf = gpd.GeoDataFrame.from_features([emel_basin])

# Оцените топологическую сложность бассейнов рек.
def calculate_complexity(gdf):
    complexity = []
    for index, row in gdf.iterrows():
        geometry = shape(row.geometry)
        # Используйте алгоритм «Сложность контура» для оценки топологической сложности.
        complexity.append(geometry.length + geometry.area / 1000)
    return complexity

sarikan_complexity = calculate_complexity(sarikan_gdf)
emel_complexity = calculate_complexity(emel_gdf)

# Сравните результаты оценок топологической сложности двух бассейнов.
print("Топологическая сложность бассейна реки Сарыкан:", sarikan_complexity[0])
print("Топологическая сложность бассейна реки Эмель:", emel_complexity[0])

# Если необходимо, создайте визуализацию на карте с помощью библиотеки Folium.
m = Map(location=[37.25, -121.875], zoom_start=10)
sarikan_polygon = Polygon(sarikan_basin['geometry']['coordinates'][0])
emel_polygon = Polygon(emel_basin['geometry']['coordinates'][0])

folium.Polygon(sarikan_polygon).add_to(m)
folium.Polygon(emel_polygon).add_to(m)

m.save("177.html")