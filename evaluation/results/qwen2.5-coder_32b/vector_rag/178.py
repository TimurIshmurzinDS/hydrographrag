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

# Предположим, что у нас есть координаты притоков реки Тентек в формате WKT
tributaries_wkt = [
    {'name': 'Tentek Tributary 1', 'geometry': wkt.loads('LINESTRING (75.0 42.0, 76.0 43.0)')},
    {'name': 'Tentek Tributary 2', 'geometry': wkt.loads('LINESTRING (74.5 41.5, 75.5 42.5)')}
]

# Добавление притоков на карту
for trib in tributaries_wkt:
    folium.PolyLine(locations=[list(coord) for coord in zip(trib['geometry'].xy[0], trib['geometry'].xy[1])],
                    color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты
m.save("178.html")