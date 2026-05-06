import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водных объектах из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с использованием центроида shapefile
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Водный бассейн", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты рек и точек наблюдения в формате WKT
coordinates = [
    {"name": "Река Тентек", "wkt": "LINESTRING (35.1 48.1, 35.2 48.2)"},
    {"name": "Река Эмель", "wkt": "LINESTRING (35.0 48.0, 35.3 48.3)"},
    {"name": "Наблюдение 0.2 км выше соединения с рекой Осек", "wkt": "POINT (35.15 48.15)"}
]

# Добавление линий и точек на карту
for coord in coordinates:
    geom = wkt.loads(coord['wkt'])
    if geom.geom_type == 'LineString':
        folium.PolyLine(locations=list(zip(geom.coords.xy[1], geom.coords.xy[0])), color='blue', weight=2.5, opacity=1).add_to(m)
    elif geom.geom_type == 'Point':
        folium.Marker(location=[geom.y, geom.x], popup=coord['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("174.html")