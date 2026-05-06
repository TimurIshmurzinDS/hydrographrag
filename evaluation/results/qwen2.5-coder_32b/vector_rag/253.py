import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Караой
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание карты с использованием центроида бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдений (примерные, так как реальные координаты не предоставлены)
observations = [
    {"name": "Observation 1", "geometry": wkt.loads("POINT(76.54321 49.87654)")},
    {"name": "Observation 2", "geometry": wkt.loads("POINT(76.55321 49.88654)")},
    {"name": "Observation 3", "geometry": wkt.loads("POINT(76.56321 49.89654)")},
    {"name": "Observation 4", "geometry": wkt.loads("POINT(76.57321 49.90654)")},
    {"name": "Observation 5", "geometry": wkt.loads("POINT(76.58321 49.91654)")}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs["name"],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("253.html")