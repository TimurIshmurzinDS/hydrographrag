import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах рек из shapefile
basins = gpd.read_file(r"data/basin_data.shp")
basins = basins.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейнов
centroid = basins.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейнов на карту
folium.GeoJson(basins.to_json(), name="Basins", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты деревни Темирлик (примерные, так как точные координаты не предоставлены)
temirlik_village_coords = [{'name': 'Temirlik village', 'geometry': wkt.loads('POINT(75.964 42.831)')}]

# Добавление деревни Темирлик на карту
for point in temirlik_village_coords:
    folium.Marker(
        location=[point['geometry'].y, point['geometry'].x],
        popup=point['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("115.html")