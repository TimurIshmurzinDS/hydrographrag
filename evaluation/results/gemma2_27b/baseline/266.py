import geopandas as gpd
from shapely.geometry import Point, LineString
from shapely.ops import nearest_points
import folium

# Загрузка данных о полях
fields = gpd.read_file("fields.shp")

# Загрузка данных о реке Караой
river = gpd.read_file("karoy.shp")

# Расчет кратчайшего расстояния до реки
distances = []
for index, row in fields.iterrows():
    point = Point(row.geometry.x, row.geometry.y)
    nearest_river_point = nearest_points(point, river.geometry)[1]
    distance = point.distance(nearest_river_point)
    distances.append(distance)

fields["distance"] = distances

# Определение зоны полива (например, расстояние до 500 метров)
fields["irrigation_zone"] = fields["distance"] <= 500

# Расчет объема воды (упрощенная версия)
fields["water_volume"] = fields.area * 0.1

# Создание карты с пометкой зон полива
m = folium.Map(location=[43.2, 76.8], zoom_start=12)
for index, row in fields.iterrows():
    if row["irrigation_zone"]:
        folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color="green").add_to(m)
    else:
        folium.CircleMarker(location=[row.geometry.y, row.geometry.x], radius=5, color="red").add_to(m)

# Сохранение карты
m.save("266.html")