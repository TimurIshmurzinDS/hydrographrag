import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.__geo_interface__, 
               name='Бассейн',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами (WKT) рек
river_coords = [
    {'name': 'Bayankol River', 'coords': wkt.loads('POLYGON ((48.1234 76.5432, 48.1245 76.5433, 48.1256 76.5434))')},
    {'name': 'Lepsy River', 'coords': wkt.loads('POLYGON ((47.6543 75.4321, 47.6554 75.4322, 47.6565 75.4323))')}
]

# Добавление рек на карту
for river in river_coords:
    folium.Polygon(river['coords'].exterior.coords[:], 
                   name=river['name'], 
                   color='blue', 
                   fill=True, 
                   fill_color='blue').add_to(m)

# Сохранение карты в файл
m.save("155.html")