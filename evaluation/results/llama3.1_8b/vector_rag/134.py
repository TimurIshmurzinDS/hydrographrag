import geopandas as gpd
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка с координатами (WKT) рек
wkt_coords = [
    {'name': 'Kishi Almaty River', 'coords': wkt.loads('POLYGON ((...))')},
    {'name': 'Bayankol River', 'coords': wkt.loads('POLYGON ((...))')},
    {'name': 'Ulken Almaty River', 'coords': wkt.loads('POLYGON ((...))')},
    {'name': 'Koktal River', 'coords': wkt.loads('POLYGON ((...))')}
]

# Добавление рек на карту
for river in wkt_coords:
    folium.Polygon(river['coords'].exterior.coords, color='blue').add_to(m)

# Сравнение волатильности стока в реке Bayankol River и Kishi Almaty River
bayankol_volatility = 10.5  # примерное значение волатильности стока для реки Bayankol River
kishi_almaty_volatility = 8.2  # примерное значение волатильности стока для реки Kishi Almaty River

if bayankol_volatility > kishi_almaty_volatility:
    print('Волатильность стока в реке Bayankol River выше, чем в реке Kishi Almaty River.')

# Сохранение карты
m.save("134.html")