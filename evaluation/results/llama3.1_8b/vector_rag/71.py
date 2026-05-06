import geopandas as gpd
import folium
from shapely import wkt

# Загрузите данные о гидрологических объектах из файла shapefile.
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создайте карту с центром в координатах средней точки области.
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте область на карту.
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.wkt,
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создайте список сенсоров, расположенных вдоль реки Byzhy River.
sensors = [
    {'name': 'Сенсор 1', 'coordinates': wkt.loads('POINT(48.6784 35.0333)')},
    {'name': 'Сенсор 2', 'coordinates': wkt.loads('POINT(48.6799 35.0345)')}
]

# Добавьте сенсоры на карту.
for sensor in sensors:
    folium.Marker(sensor['coordinates'], popup=sensor['name']).add_to(m)

# Сохраните карту в файл.
m.save("71.html")