import geopandas as gpd
import folium
from shapely import wkt

# Загрузить гео-пространственные данные о реке Koktal River в формате shapefile.
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту с центром в середине области и параметрами tiles='CartoDB positron'.
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавить область на карте.
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создать список точек (постов) на реке Koktal River.
points = [
    {'location': [46.1234, 68.9012], 'level': 10},
    {'location': [46.2345, 69.0123], 'level': 15}
]

# Добавить маркеры для каждого поста на карте с информацией о уровне воды.
for point in points:
    folium.Marker(point['location'], popup=f'Уровень воды: {point["level"]} см').add_to(m)

# Сохранить карту в файл html.
m.save("88.html")