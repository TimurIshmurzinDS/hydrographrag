import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Караой
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Караой
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin.to_json(), name="Караой Река", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек полива (примерные координаты, так как точные не предоставлены)
irrigation_points = [
    {"name": "Точка 1", "coordinates": wkt.loads("POINT(75.3456 42.8901)")},
    {"name": "Точка 2", "coordinates": wkt.loads("POINT(75.3567 42.8890)")},
    {"name": "Точка 3", "coordinates": wkt.loads("POINT(75.3678 42.8880)")}
]

# Добавление точек полива на карту
for point in irrigation_points:
    folium.Marker(
        location=[point["coordinates"].y, point["coordinates"].x],
        popup=point["name"],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("266.html")