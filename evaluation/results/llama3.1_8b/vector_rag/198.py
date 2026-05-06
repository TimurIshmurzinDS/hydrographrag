import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах рек из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн реки',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений (предположительно, данные о водном уровне)
observations = [
    {"location": "аул Lepsy", "water_level": 10},
    {"location": "аул Lepsy", "water_level": 12},
    {"location": "аул Lepsy", "water_level": 11}
]

# Визуализация наблюдений на карте
for observation in observations:
    folium.Marker(location=[observation["location"].latitude, observation["location"].longitude],
                  popup=f"Уровень воды: {observation['water_level']}").add_to(m)

# Сохранение карты в файл
m.save("198.html")