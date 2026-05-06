import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Или
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если бы у нас были координаты наблюдений в формате WKT, мы добавили их следующим образом:
# observations = [
#     {"name": "near Ili", "geometry": wkt.loads("POINT(79.85 46.05)")},
#     {"name": "upper Ili area", "geometry": wkt.loads("POINT(80.15 46.35)")}
# ]
# for obs in observations:
#     folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Сохранение карты в файл
m.save("9.html")