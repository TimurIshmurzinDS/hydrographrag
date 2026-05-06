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

# Координаты наблюдений (если бы они были предоставлены в формате WKT)
# Например:
# observations = [
#     {"name": "Tekeli town", "geometry": wkt.loads("POINT(38.75 41.05)")}
# ]

# Добавление точек наблюдений на карту (если бы они были предоставлены)
# for obs in observations:
#     folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Сохранение карты
m.save("116.html")