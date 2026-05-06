import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о границе водного бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границы водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о потреблении воды и урожайности (заменить на реальные данные)
data_points = [
    {"coordinates": "POINT(48.35 61.75)", "water_consumption": 1500, "yield": 20},
    {"coordinates": "POINT(48.40 61.80)", "water_consumption": 2000, "yield": 25},
    {"coordinates": "POINT(48.37 61.78)", "water_consumption": 1800, "yield": 22}
]

# Добавление точек на карту
for point in data_points:
    coord = wkt.loads(point["coordinates"])
    folium.Marker(
        location=[coord.y, coord.x],
        popup=f"Потребление воды: {point['water_consumption']} м³, Урожайность: {point['yield']} ц/га"
    ).add_to(m)

# Сохранение карты в файл
m.save("185.html")