import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если бы были координаты (WKT), они были бы добавлены следующим образом:
# coordinates = [
#     {"name": "Kurty River", "wkt": "LINESTRING(...)"}, 
#     {"name": "Sharyn River", "wkt": "LINESTRING(...)"}
# ]
# for coord in coordinates:
#     geom = wkt.loads(coord["wkt"])
#     folium.GeoJson(geom, name=coord["name"]).add_to(m)

# Сохранение карты
m.save("123.html")