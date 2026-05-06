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

# Если есть координаты точек наблюдения (WKT), добавляем их на карту
observations = [
    {"name": "Akzhar aul", "geometry": wkt.loads("POINT(81.375469 40.283333)")}  # Примерные координаты для иллюстрации
]

for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs["name"],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("117.html")