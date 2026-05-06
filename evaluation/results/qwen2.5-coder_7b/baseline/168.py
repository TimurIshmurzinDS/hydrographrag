import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium

# Загрузка данных
basin_emel = gpd.read_file('path_to_basin_emel.shp')
river_sarykan = gpd.read_file('path_to_river_sarykan.shp')

# Определение бассейна реки Эмель (пример: простой полигон)
# basin_emel = gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (1, 1), (1, 0)])])

# Определение притоков реки Сарыкан
pritoki_sarykan = river_sarykan[river_sarykan.geometry.within(basin_emel.unary_union)]

# Визуализация результатов
m = folium.Map(location=[basin_emel.centroid.y.mean(), basin_emel.centroid.x.mean()], zoom_start=10)

folium.GeoJson(basin_emel, name='Basin Emel').add_to(m)
folium.GeoJson(pritoki_sarykan, name='Pritoki Sarykan').add_to(m)

folium.LayerControl().add_to(m)

# Сохранение карты
m.save("168.html")