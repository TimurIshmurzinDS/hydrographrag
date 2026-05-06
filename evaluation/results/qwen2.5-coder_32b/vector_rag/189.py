import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна реки Турген
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Турген
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если бы были координаты (WKT), они были бы добавлены следующим образом:
# coordinates = [{'name': 'Tauturgen village', 'wkt': 'POINT(75.934167 42.805556)'}]  # Пример координат
# for coord in coordinates:
#     point = wkt.loads(coord['wkt'])
#     folium.Marker([point.y, point.x], popup=coord['name']).add_to(m)

# Сохранение карты в файл
m.save("189.html")