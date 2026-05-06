import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Аягоз из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна реки на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты городов и точек наблюдений (если есть)
observations = [
    {"name": "Ayagoz city", "coordinates": wkt.loads("POINT(45.123 40.456)")}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=obs['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("35.html")