import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# 2. Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
centroid = basin_data.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# 3. Добавление бассейна на карту с прозрачностью 20%
basin_geojson = basin_data.to_crs(epsg=3857).to_json()
folium.GeoJson(basin_geojson, name='basin').add_to(m)

# 4. Создание списка гидропостов (поскольку в задаче нет точек данных о гидропостах)
hydro_posts = [
    {'name': 'Гидропост 1', 'location': [55.123456, 37.654321]},
    {'name': 'Гидропост 2', 'location': [54.987654, 38.765432]}
]

# 5. Добавление гидропостов на карту
for hydro_post in hydro_posts:
    folium.Marker(hydro_post['location'], popup=hydro_post['name']).add_to(m)

# 6. Создание списка наблюдений (поскольку в задаче нет точных данных о наблюдениях)
observations = [
    {'date': '2022-03-01', 'water_consumption': 100, 'water_level': 80},
    {'date': '2022-04-15', 'water_consumption': 120, 'water_level': 90}
]

# 7. Добавление наблюдений на карту
for observation in observations:
    folium.Marker([observation['location'][0], observation['location'][1]], popup=f'Дата: {observation["date"]}\nРасход воды: {observation["water_consumption"]} м³\nУровень воды: {observation["water_level"]} %').add_to(m)

# 8. Сохранение карты в файл
m.save("84.html")