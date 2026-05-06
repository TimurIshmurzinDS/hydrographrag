import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границ бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Создание списка координат наблюдений (если они есть)
observations = [
    {'wkt': 'POINT(74.5678 43.1234)', 'color': 'red', 'radius': 5},
    {'wkt': 'POINT(74.5679 43.1235)', 'color': 'blue', 'radius': 5},
    {'wkt': 'POINT(74.5680 43.1236)', 'color': 'green', 'radius': 5}
]

# Добавление точек наблюдения на карту
for obs in observations:
    point = wkt.loads(obs['wkt'])
    folium.CircleMarker(
        location=[point.y, point.x],
        radius=obs['radius'],
        color=obs['color'],
        fill=True,
        fill_color=obs['color']
    ).add_to(m)

# Сохранение карты
m.save("8.html")