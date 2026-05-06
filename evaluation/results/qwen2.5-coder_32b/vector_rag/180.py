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
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть координаты реки Текес в формате WKT
tekes_coords = [
    {"name": "Текес", "wkt": "LINESTRING(86.953125 42.703125, 87.053125 42.803125, 87.153125 42.903125)"}
]

# Добавление реки Текес на карту
for feature in tekas_coords:
    geom = wkt.loads(feature['wkt'])
    folium.GeoJson(gpd.GeoSeries(geom, crs='EPSG:4326').to_json(), name=feature['name'], style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Предположим координаты точки слияния рек Текес и Сарыкан
confluence_coords = wkt.loads("POINT(87.103125 42.953125)")
folium.Marker([confluence_coords.y, confluence_coords.x], popup="Слияние Текес и Сарыкан", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("180.html")