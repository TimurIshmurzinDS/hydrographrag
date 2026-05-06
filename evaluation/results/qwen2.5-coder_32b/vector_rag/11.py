import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна и преобразование в CRS EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с центром, соответствующим центроиду бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами точек наблюдения (если они есть)
observations = [
    {"name": "0.2 km above the confluence with Osek River", "geometry": wkt.loads("POINT(78.5 43.1)")}  # Примерные координаты
]

# Добавление точек наблюдения на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs["name"],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("11.html")