import geopandas as gpd
from shapely.geometry import Point
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть GeoDataFrame с реками и пастбищами.
# Для примера создадим эти данные искусственно.

# Координаты рек
byzhy_river_coords = [(42.8500, 74.6100), (42.8600, 74.6200)]
lepsy_river_coords = [(43.0000, 74.7000), (43.0100, 74.7100)]

# Координаты пастбищ
pastures_coords = [
    (42.8550, 74.6150),
    (42.8650, 74.6250),
    (43.0050, 74.7050),
    (43.0150, 74.7150)
]

# Создание GeoDataFrame для рек
byzhy_river = gpd.GeoSeries([Point(coords) for coords in byzhy_river_coords])
lepsy_river = gpd.GeoSeries([Point(coords) for coords in lepsy_river_coords])

# Создание GeoDataFrame для пастбищ
pastures = gpd.GeoSeries([Point(coords) for coords in pastures_coords])

# Шаг 2: Обработка данных
byzhy_river_gdf = gpd.GeoDataFrame(geometry=byzhy_river)
lepsy_river_gdf = gpd.GeoDataFrame(geometry=lepsy_river)
pastures_gdf = gpd.GeoDataFrame(geometry=pastures)

# Шаг 3: Анализ доступности воды
# Вычисление расстояний от пастбищ до рек

distances_byzhy = pastures_gdf.distance(byzhy_river_gdf.unary_union)
distances_lepsy = pastures_gdf.distance(lepsy_river_gdf.unary_union)

pastures_gdf['distance_to_byzhy'] = distances_byzhy
pastures_gdf['distance_to_lepsy'] = distances_lepsy

# Шаг 4: Визуализация результатов
m = folium.Map(location=[42.9300, 74.6500], zoom_start=11)

# Добавление рек на карту
folium.PolyLine(byzhy_river_coords, color="blue", weight=2.5, opacity=1).add_to(m)
folium.PolyLine(lepsy_river_coords, color="green", weight=2.5, opacity=1).add_to(m)

# Добавление пастбищ на карту с метками расстояний
for idx, row in pastures_gdf.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=f"Расстояние до Byzhy: {row['distance_to_byzhy']:.2f} м\n"
              f"Расстояние до Lepsy: {row['distance_to_lepsy']:.2f} м",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("109.html")