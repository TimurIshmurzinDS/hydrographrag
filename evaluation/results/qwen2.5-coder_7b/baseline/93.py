import geopandas as gpd
from shapely.geometry import Point, LineString
import folium

# Загрузка данных о реках (пример: используем GeoJSON)
rivers_gdf = gpd.read_file('path_to_your_rivers_data.geojson')

# Фильтрация притоков реки Каратал
kara_tal_id = rivers_gdf[rivers_gdf['name'] == 'Каратал'].index[0]
outlets = rivers_gdf[(rivers_gdf['parent'] == kara_tal_id) & (rivers_gdf['type'] == 'outlet')]

# Вычисление общей протяженности притоков
total_length = outlets.geometry.length.sum()
print(f"Общая протяженность притоков реки Каратал: {total_length} м")

# Визуализация на карте
m = folium.Map(location=[rivers_gdf['geometry'].centroid.y.mean(), rivers_gdf['geometry'].centroid.x.mean()], zoom_start=10)

# Добавление всех рек на карту
folium.GeoJson(rivers_gdf.to_json()).add_to(m)

# Добавление притоков реки Каратал на карту
outlets_layer = folium.FeatureGroup(name='Притоки реки Каратал')
for _, row in outlets.iterrows():
    folium.Marker([row['geometry'].y, row['geometry'].x], popup=row['name']).add_to(outlets_layer)
outlets_layer.add_to(m)

# Добавление слоя управления
folium.LayerControl().add_to(m)

# Сохранение карты
m.save("93.html")