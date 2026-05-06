import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование CRS
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в полигоне бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты наблюдений в формате WKT
observations = [
    {"name": "upper Ili area", "wkt": "POINT(87.654 43.123)", "water_level": 1050},
    {"name": "near Ili", "wkt": "POINT(87.987 43.456)", "water_level": 1045}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"{obs['name']}: Уровень воды {obs['water_level']} м",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("1.html")