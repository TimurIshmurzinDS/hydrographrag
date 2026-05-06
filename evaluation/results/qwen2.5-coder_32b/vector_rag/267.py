import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), добавляем их на карту
coordinates = [
    {"name": "Наблюдение на расстоянии 0.2 км выше соединения с рекой Осек", "wkt": "POINT(45.321 69.123)"}
]

for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты
m.save("267.html")