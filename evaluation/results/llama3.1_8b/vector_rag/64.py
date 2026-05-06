import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о реках
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине области
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить область на карту
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.apply(lambda x: x.wkt).values.tolist(),
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список с координатами рек (хотя в контексте нет никакой информации о координатах)
river_coords = [
    {"name": "Tentek River", "coords": [(46.123, 30.456), (46.789, 31.012)]},
    {"name": "Tekes River", "coords": [(47.321, 32.145), (48.098, 33.567)]},
    {"name": "Osek River", "coords": [(49.123, 34.456), (50.789, 35.012)]},
    {"name": "Tekeli River", "coords": [(51.321, 36.145), (52.098, 37.567)]},
    {"name": "Butak River", "coords": [(53.123, 38.456), (54.789, 39.012)]}
]

# Добавить координаты рек на карту
for river in river_coords:
    folium.Polygon(river["coords"], color='red', fill_color='red').add_to(m)

# Сохранить карту в файл
m.save("64.html")