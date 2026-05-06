import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне рек
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты точек наблюдений (пример)
observation_points = [
    {"name": "Shyzhyn River", "coordinates": wkt.loads("POINT(87.6543 49.1234)"), "water_level_values": [100, 120, 110, 130, 140]},
    {"name": "Ili River", "coordinates": wkt.loads("POINT(87.6543 49.1234)"), "water_level_values": [150, 160, 170, 180, 190]}
]

# Добавление точек наблюдений на карту
for point in observation_points:
    folium.Marker(
        location=[point["coordinates"].y, point["coordinates"].x],
        popup=f"{point['name']} - Water Levels: {point['water_level_values']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("160.html")