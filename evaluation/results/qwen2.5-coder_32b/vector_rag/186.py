import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile бассейна реки Бутак
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Бутак
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Бассейн реки Бутак",
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что координаты сельского хозяйства (Butak village) известны и представлены в формате WKT
# В данном примере создадим список словарей с координатами точек наблюдений
observations = [
    {'name': 'Наблюдение 1', 'geometry': wkt.loads('POINT(37.5 46.0)')},
    {'name': 'Наблюдение 2', 'geometry': wkt.loads('POINT(37.6 46.1)')},
    {'name': 'Наблюдение 3', 'geometry': wkt.loads('POINT(37.55 46.05)')},
    {'name': 'Наблюдение 4', 'geometry': wkt.loads('POINT(37.65 46.15)')}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("186.html")