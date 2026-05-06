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

# Предположим, что у нас есть координаты реки Шынжалы в формате WKT
shynzhaly_coords = "LINESTRING(86.953125 47.916667, 87.000000 47.950000)"  # Примерные координаты для демонстрации
shynzhaly_geom = wkt.loads(shynzhaly_coords)

# Создание слоя с рекой Шынжалы
folium.GeoJson(gpd.GeoSeries([shynzhaly_geom], crs='EPSG:4326').to_json(), name="Shynzhaly River", style_function=lambda x: {'color': 'blue', 'weight': 3}).add_to(m)

# Добавление маркера с информацией о водном качестве и уровне воды
popup_text = "Река Шынжалы\nКласс водного качества: III\nУровень воды: 1.2 м"
folium.Marker(location=[shynzhaly_geom.centroid.y, shynzhaly_geom.centroid.x], popup=popup_text, icon=folium.Icon(color='blue')).add_to(m)

# Сохранение карты
m.save("44.html")