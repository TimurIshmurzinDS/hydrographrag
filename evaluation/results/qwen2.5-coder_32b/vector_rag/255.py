import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Каскелен
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Получение центроида для установки центра карты
centroid = basin_data.geometry.centroid.iloc[0]

# Создание интерактивной карты
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна реки Каскелен на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Сохранение карты в HTML файл
m.save("255.html")