import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание карты с центром в бассейне
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты наблюдений (WKT)
observations = [
    {"id": "Observation_2190", "year": 1890, "geometry": wkt.loads("POINT(37.6173 55.7558)"), "gold_mined": 100},  # Примерные координаты Москвы
    {"id": "Observation_2199", "year": 1899, "geometry": wkt.loads("POINT(37.6173 55.7558)"), "gold_mined": 120},
    {"id": "Observation_2279", "year": 1979, "geometry": wkt.loads("POINT(37.6173 55.7558)"), "gold_mined": 400},
    {"id": "Observation_2219", "year": 1919, "geometry": wkt.loads("POINT(37.6173 55.7558)"), "gold_mined": 150},
    {"id": "Observation_2200", "year": 1900, "geometry": wkt.loads("POINT(37.6173 55.7558)"), "gold_mined": 130}
]

# Добавление точек наблюдений на карту
for obs in observations:
    color = 'blue' if obs['year'] < 1900 else 'red'
    folium.CircleMarker(
        location=[obs['geometry'].y, obs['geometry'].x],
        radius=5,
        popup=f"{obs['id']} ({obs['year']}): {obs['gold_mined']} тонн золота",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Сохранение карты в файл
m.save("274.html")