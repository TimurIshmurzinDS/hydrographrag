import folium
from folium.plugins import SearchLayerControl

# Загрузите географические данные о реке Емель и ее притоках.
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Создайте базу данных OpenStreetMap (OSM) или другую географическую базу данных.
gdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Определите реки Емель и Быж в базе данных OSM.
river_emel = gdf[gdf['name'] == 'Емель']
river_byzh = gdf[gdf['name'] == 'Быж']

# Создайте карту с помощью библиотеки Folium.
m = folium.Map(location=[55.0, 85.0], zoom_start=6)

# Добавьте на карту реки Емель и Быж.
folium.Marker([river_emel.geometry.y.mean(), river_emel.geometry.x.mean()], popup='Река Емель').add_to(m)
folium.Marker([river_byzh.geometry.y.mean(), river_byzh.geometry.x.mean()], popup='Река Быж').add_to(m)

# Добавьте на карту информацию о притоках реки Емель.
for index, row in river_emel.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row['name']).add_to(m)

# Сохраните карту в файле HTML.
m.save("101.html")