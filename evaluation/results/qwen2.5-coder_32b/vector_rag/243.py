import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Кумбель из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в точке, соответствующей центроиду бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат реки Кумбель в формате WKT (для демонстрации)
river_coordinates_wkt = "LINESTRING (37.5 56.1, 38.0 56.2, 38.5 56.3)"
river_geometry = wkt.loads(river_coordinates_wkt)

# Добавление линии реки на карту
folium.GeoJson(gpd.GeoSeries([river_geometry]).to_json(), name="Kumbel River", style_function=lambda x: {'color': 'blue', 'weight': 3}).add_to(m)

# Сохранение карты в файл
m.save("243.html")