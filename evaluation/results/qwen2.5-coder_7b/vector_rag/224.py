import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Создание карты с центром в centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример добавления данных о реке Karaoy River (если есть координаты WKT)
karaoy_river_wkt = "LINESTRING(105.1234 40.5678, 105.1235 40.5679)"  # Пример WKT
karaoy_river_geom = wkt.loads(karaoy_river_wkt)
folium.GeoJson(folium.features.GeoJsonGeometryCollection([karaoy_river_geom]), style_function=lambda x: {
    'color': 'blue',
    'weight': 2,
    'opacity': 1
}).add_to(m)

# Сохранение карты
m.save("224.html")