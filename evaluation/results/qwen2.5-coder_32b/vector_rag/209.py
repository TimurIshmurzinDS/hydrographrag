import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Уржар
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Уржар
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат точек наблюдений (WKT)
observations = [
    {"name": "Observation_2264", "geometry": wkt.loads("POINT(51.3789 51.1234)")},
    {"name": "Observation_2247", "geometry": wkt.loads("POINT(51.3800 51.1256)")},
    {"name": "Observation_2265", "geometry": wkt.loads("POINT(51.3795 51.1245)")}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs["name"],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("209.html")