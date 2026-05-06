import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Лепсы
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты наблюдательных пунктов (WKT), добавить их на карту
# В данном случае, координаты не предоставлены, поэтому создаем примерный список
observations = [
    {'name': 'аул Lepsy 1', 'geometry': wkt.loads('POINT(45.0 42.0)')},
    {'name': 'аул Lepsy 2', 'geometry': wkt.loads('POINT(45.1 42.1)')},
    {'name': 'аул Lepsy 3', 'geometry': wkt.loads('POINT(45.2 42.2)')},
    {'name': 'аул Lepsy 4', 'geometry': wkt.loads('POINT(45.3 42.3)')}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("205.html")