import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import folium

# 1. Загрузка данных о уровне воды (замените на актуальный источник)
water_levels = pd.read_csv("water_levels_prokhodnaya.csv")

# 2. Обработка данных (предполагается, что данные содержат координаты и уровень воды)
water_levels['geometry'] = water_levels.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
gdf_water_levels = gpd.GeoDataFrame(water_levels, geometry='geometry')

# 3. Загрузка слоя реки (замените на актуальный путь к файлу)
river = gpd.read_file("prokhodnaya_river.shp")

# 4. Интерполяция данных (пример с IDW)
from scipy.interpolate import idw
x, y, z = gdf_water_levels['geometry'].x, gdf_water_levels['geometry'].y, gdf_water_levels['water_level']
xi, yi = river.geometry.apply(lambda geom: geom.x).values, river.geometry.apply(lambda geom: geom.y).values
zi = idw(x, y, z, xi, yi)

# 5. Визуализация на карте
m = folium.Map(location=[river.unary_union.centroid.y, river.unary_union.centroid.x], zoom_start=12)
folium.GeoJson(river).add_to(m)

# Добавление цветовой шкалы для уровня воды (пример)
color_scale = folium.colormap.LinearColormap(colors=['blue', 'green', 'yellow'], vmin=z.min(), vmax=z.max())
folium.GeoJson(river, style_function=lambda feature: {
    'fillColor': color_scale(zi[feature['properties']['id']]),
}).add_to(m)

m.save("5.html")