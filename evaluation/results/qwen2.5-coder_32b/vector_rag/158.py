import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне рек
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в бассейне рек
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдательных пунктов (примерные, так как реальные координаты не предоставлены)
observations = [
    {"name": "Bayankol village", "coordinates": wkt.loads("POINT(87.654 49.123)")},
    {"name": "Bayankol village", "coordinates": wkt.loads("POINT(87.655 49.124)")},
    {"name": "Bayankol village", "coordinates": wkt.loads("POINT(87.656 49.125)")}
]

# Добавление маркеров наблюдательных пунктов на карту
for obs in observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=obs["name"],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("158.html")