import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна реки Или из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление маркера с сообщением о необходимости проверки данных
folium.Marker(
    location=[centroid.y, centroid.x],
    popup="Необходимо проверить наличие оповещений от датчиков уровня воды.",
    icon=folium.Icon(color='red')
).add_to(m)

# Сохранение карты в файл
m.save("144.html")