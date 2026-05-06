import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Каскелен
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Каскелен
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты города Каскелен (примерные, так как точных координат нет в контексте)
kaskelen_coords = [{'name': 'Kaskelen city', 'coordinates': wkt.loads('POINT(71.4360 51.1298)')}]

# Добавление маркера для города Каскелен на карту
for point in kaskelen_coords:
    folium.Marker(
        location=[point['coordinates'].y, point['coordinates'].x],
        popup=point['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("240.html")