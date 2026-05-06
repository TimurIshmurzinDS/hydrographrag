import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование в CRS EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с центром, соответствующим центроиду бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты истоков рек (в реальности эти данные должны быть загружены из надежного источника)
river_sources = [
    {'name': 'Улькен Алматы', 'coordinates': wkt.loads('POINT(76.923058 42.884168)')},  # Примерные координаты
    {'name': 'Уржар', 'coordinates': wkt.loads('POINT(76.850000 42.900000)')}          # Примерные координаты
]

# Добавление маркеров на карту для истоков рек
for source in river_sources:
    folium.Marker(
        location=[source['coordinates'].y, source['coordinates'].x],
        popup=source['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в HTML файл
m.save("99.html")