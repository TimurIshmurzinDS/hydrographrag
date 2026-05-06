import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Инициализация карты с центром в бассейне и стилем 'CartoDB positron'
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты русел рек в формате WKT (для примера)
river_coordinates = [
    {"name": "Shynzhaly River", "wkt": "LINESTRING(76.95 43.05, 77.00 43.10, 77.05 43.15)"},
    {"name": "Talgar River", "wkt": "LINESTRING(76.98 43.08, 77.02 43.12, 77.06 43.16)"}
]

# Создание GeoDataFrame для русел рек
rivers_gdf = gpd.GeoDataFrame(
    river_coordinates,
    geometry=[wkt.loads(r['wkt']) for r in river_coordinates],
    crs="EPSG:4326"
)

# Добавление линий русел на карту
for _, row in rivers_gdf.iterrows():
    folium.GeoJson(row.geometry, name=row.name).add_to(m)

# Выполнение операции пересечения между руслами рек Шынжалы и Талгар
shynzhaly = rivers_gdf[rivers_gdf['name'] == 'Shynzhaly River'].geometry.iloc[0]
talgar = rivers_gdf[rivers_gdf['name'] == 'Talgar River'].geometry.iloc[0]
intersection = shynzhaly.intersection(talgar)

# Добавление результата пересечения на карту
if not intersection.is_empty:
    folium.GeoJson(intersection, name="Intersection", style_function=lambda x: {'color': 'red', 'weight': 3}).add_to(m)

# Сохранение карты в HTML файл
m.save("169.html")