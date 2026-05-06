import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Токыраун
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Tokyraun Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты некоторых животноводческих хозяйств в формате WKT
farms_wkt = [
    "POINT (39.184331 56.852271)",
    "POINT (39.204331 56.862271)",
    "POINT (39.194331 56.872271)"
]

# Преобразование WKT в геометрические объекты и добавление на карту
farms = [wkt.loads(wkt_str) for wkt_str in farms_wkt]
for farm in farms:
    folium.Marker([farm.y, farm.x], popup="Животноводческое хозяйство").add_to(m)

# Сохранение карты в HTML файл
m.save("187.html")