import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реках и границы бассейна
temirlik_river = gpd.GeoDataFrame({'geometry': [wkt.loads('LINESTRING(10 20, 30 40)')]})
turgen_river = gpd.GeoDataFrame({'geometry': [wkt.loads('LINESTRING(50 60, 70 80)')]})

basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Добавление рек на карту
folium.GeoJson(temirlik_river.to_json()).add_to(m)
folium.GeoJson(turgen_river.to_json()).add_to(m)

# Сохранение карты
m.save("83.html")