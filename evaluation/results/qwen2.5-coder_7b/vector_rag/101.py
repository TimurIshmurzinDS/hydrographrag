import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Инициализация карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты начал притоков рек (WKT)
prong_sources = [
    {"name": "Тентек", "wkt": "POINT(37.5 41.5)"},
    {"name": "Быж", "wkt": "POINT(38.0 42.0)"}
]

# Преобразование WKT в объекты Shapely
prong_sources_geom = [wkt.loads(source["wkt"]) for source in prong_sources]

# Проверка, является ли начало одной из рек притоком другой
for i, source1 in enumerate(prong_sources_geom):
    for j, source2 in enumerate(prong_sources_geom):
        if i != j and source1.within(source2.buffer(0.1)):
            print(f"{prong_sources[i]['name']} является притоком {prong_sources[j]['name']}")

# Сохранение карты
m.save("101.html")