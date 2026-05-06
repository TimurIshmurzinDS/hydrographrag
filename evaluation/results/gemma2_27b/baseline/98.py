import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузить данные о реках
rivers = gpd.read_file("path/to/rivers.shp")

# Загрузить DEM (цифровую модель поверхности)
dem = gpd.read_file("path/to/dem.tif")

# Определить водораздел
watershed = dem.watershed(rivers)

# Проследить путь рек
river_paths = rivers.apply(lambda row: gpd.GeoDataFrame({"geometry": [row.geometry]}, crs=rivers.crs))

# Определить бассейн впадания
for river in river_paths:
    if river.intersects(watershed):
        print(f"Река {river.name} впадает в бассейн {watershed}")

# Визуализация на карте
m = folium.Map(location=[rivers.geometry.y.mean(), rivers.geometry.x.mean()], zoom_start=10)

# Добавить реки на карту
folium.GeoJson(rivers).add_to(m)

# Добавить водораздел на карту
folium.GeoJson(watershed, style_function=lambda feature: {"color": "blue", "weight": 2}).add_to(m)

# Сохранить карту
m.save("98.html")