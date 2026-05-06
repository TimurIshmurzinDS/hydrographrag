import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Турген
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты наблюдений в формате WKT
observations_wkt = [
    "POINT(87.6543 42.9876)",
    "POINT(87.6550 42.9880)",
    "POINT(87.6555 42.9885)",
    "POINT(87.6560 42.9890)"
]

# Преобразование WKT в геометрические объекты
observations = [{'geometry': wkt.loads(wkt_str)} for wkt_str in observations_wkt]
observations_gdf = gpd.GeoDataFrame(observations, crs='EPSG:4326')

# Добавление наблюдений на карту
for _, row in observations_gdf.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup="Наблюдение").add_to(m)

# Сохранение карты в файл
m.save("183.html")