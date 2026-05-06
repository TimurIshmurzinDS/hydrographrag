import geopandas as gpd
import folium
from shapely import wkt

# 1. Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# 2. Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# 3. Добавить бассейн на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# 4. Создать hardcoded список словарей для координат и границ рек
river_data = [
    {'name': 'Shynzhaly River', 'coordinates': wkt.loads('SRID=4326;GEOMETRYFROMTEXT("LINESTRING(48.6781 35.2345, 48.6792 35.2357)")')},
    {'name': 'Shyzhyn River', 'coordinates': wkt.loads('SRID=4326;GEOMETRYFROMTEXT("LINESTRING(48.6823 35.2389, 48.6834 35.2401)")')}
]

# 5. Добавить реки на карту
for river in river_data:
    folium.Polygon(river['coordinates'].exterior.coords[:], color='blue', fill_color='lightblue').add_to(m)

# 6. Сохранить карту в файл
m.save("154.html")