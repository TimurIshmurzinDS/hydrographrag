import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне Сарыкан-реки
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне Сарыкан-реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты некоторых точек наблюдений (WKT)
observations = [
    {"name": "Наблюдение 1", "geometry": wkt.loads("POINT(75.3456 48.2345)")},
    {"name": "Наблюдение 2", "geometry": wkt.loads("POINT(75.4567 48.3456)")},
    {"name": "Наблюдение 3", "geometry": wkt.loads("POINT(75.5678 48.4567)")}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("153.html")