import geopandas as gpd
from shapely.geometry import shape
import folium

# Загрузите данные о реках в формате Shapefile (.shp)
gdf = gpd.read_file('реки.shp')

# Определите притоки реки Каратал
pritoki_karatal = gdf[gdf['name'] == 'Каратал']

# Используйте функцию sjoin для поиска притоков реки Каратал
gdf_pritoki = gpd.sjoin(gdf, pritoki_karatal, how='inner', op='intersects')

# Рассчитайте общую длину притоков реки Каратал
dliny_prutokov = gdf_pritoki['geometry'].length.sum()

print(f'Общая длина притоков реки Каратал: {dliny_prutokov:.2f} км')

# Если требуется визуализация на карте, используйте библиотеку folium
m = folium.Map(location=[45.0, 75.0], zoom_start=6)

# Добавьте геометрии притоков реки Каратал на карту
folium.GeoJson(gdf_pritoki['geometry'].apply(lambda x: shape(x).wkt)).add_to(m)

# Сохраните карту как HTML-файл
m.save("93.html")