import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о наблюдениях (заменить на реальные данные)
observations = [
    {"name": "above Bartogay Reservoir", "coordinates": wkt.loads("POINT(45.123 60.456)"), "water_level_value": 180, "date_water_level_value": "2023-10-01"},
    {"name": "above Bartogay Reservoir", "coordinates": wkt.loads("POINT(45.789 60.123)"), "water_level_value": 190, "date_water_level_value": "2023-10-01"},
    {"name": "above Bartogay Reservoir", "coordinates": wkt.loads("POINT(45.456 60.789)"), "water_level_value": 200, "date_water_level_value": "2023-10-01"}
]

# Определение критерия повышенного уровня воды (например, выше среднего)
average_water_level = sum(obs['water_level_value'] for obs in observations) / len(observations)
elevated_observations = [obs for obs in observations if obs['water_level_value'] > average_water_level]

# Добавление точек с повышенным уровнем воды на карту
for obs in elevated_observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=f"Наблюдение: {obs['name']}<br>Уровень воды: {obs['water_level_value']}<br>Дата: {obs['date_water_level_value']}",
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты
m.save("148.html")