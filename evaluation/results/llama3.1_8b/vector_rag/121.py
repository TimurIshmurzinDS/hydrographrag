import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='Бассейн',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка наблюдений
observations = [
    {"id": 1, "name": "Село Баянколь", "water_flow": 10},
    {"id": 2, "name": "Село Баянколь", "water_flow": 15},
    {"id": 3, "name": "Село Баянколь", "water_flow": 20}
]

# Создание списка наблюдений для реки Shilik River
shilik_observations = [
    {"id": 1, "name": "Река Шилик", "water_flow": 5},
    {"id": 2, "name": "Река Шилик", "water_flow": 10},
    {"id": 3, "name": "Река Шилик", "water_flow": 15}
]

# Рассчет среднего расхода воды
bayankol_avg_water_flow = sum(obs["water_flow"] for obs in observations) / len(observations)
shilik_avg_water_flow = sum(obs["water_flow"] for obs in shilik_observations) / len(shilik_observations)

print(f"Средний расход воды в реке Bayankol River: {bayankol_avg_water_flow}")
print(f"Средний расход воды в реке Shilik River: {shilik_avg_water_flow}")

# Сохранение карты
m.save("121.html")