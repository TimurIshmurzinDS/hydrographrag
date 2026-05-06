import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных
river = gpd.read_file("path/to/river_data.shp")
farms = gpd.read_file("path/to/farm_data.shp")

# Расчет расстояния до реки
farms["distance_to_river"] = farms.geometry.apply(lambda x: river.nearest(x).distance(x))

# Классификация по близости
bins = [0, 5000, 10000, float("inf")]
labels = ["close", "medium", "far"]
farms["river_proximity"] = pd.cut(farms["distance_to_river"], bins=bins, labels=labels)

# Визуализация
m = folium.Map(location=[river.geometry.apply(lambda x: x.y).mean(), river.geometry.apply(lambda x: x.x).mean()], zoom_start=10)

# Добавление слоя реки
folium.GeoJson("path/to/river_data.shp").add_to(m)

# Добавление слоя ферм с цветом в зависимости от близости к реке
for index, row in farms.iterrows():
    color = {"close": "green", "medium": "yellow", "far": "red"}[row["river_proximity"]]
    folium.Marker(location=[row.geometry.y, row.geometry.x], popup=f"Farm ID: {index}", color=color).add_to(m)

# Сохранение карты
m.save("187.html")