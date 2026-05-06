import geopandas as gpd
from shapely.geometry import Point
import folium

# Загрузка данных о реках из открытых источников
rivers = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres_water'))

# Фильтрация рек по названию
tentek_river = rivers[rivers['name'].str.contains('Tentek', na=False, case=False)]
byzh_river = rivers[rivers['name'].str.contains('Byzh', na=False, case=False)]

# Если данные о реках не найдены, можно использовать примерные координаты
if tentek_river.empty:
    tentek_point = Point(43.25, 46.0)  # Примерные координаты Тентека
    tentek_gdf = gpd.GeoDataFrame(geometry=[tentek_point], crs=rivers.crs)
else:
    tentek_gdf = tentek_river

if byzh_river.empty:
    byzh_point = Point(43.5, 46.2)  # Примерные координаты Быжа
    byzh_gdf = gpd.GeoDataFrame(geometry=[byzh_point], crs=rivers.crs)
else:
    byzh_gdf = byzh_river

# Загрузка данных о гидрографических бассейнах (примерные данные, можно использовать более точные источники)
basins = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Определение бассейнов для рек
tentek_basin = basins[basins.contains(tentek_gdf.geometry.iloc[0])]
byzh_basin = basins[basins.contains(byzh_gdf.geometry.iloc[0])]

# Вывод результатов
print(f"Река Тентек впадает в бассейн: {tentek_basin['name'].values[0]}")
print(f"Река Быж впадает в бассейн: {byzh_basin['name'].values[0]}")

# Визуализация на карте
m = folium.Map(location=[46.1, 43.4], zoom_start=8)

folium.GeoJson(tentek_gdf).add_to(m)
folium.GeoJson(byzh_gdf).add_to(m)
folium.GeoJson(tentek_basin).add_to(m)
folium.GeoJson(byzh_basin).add_to(m)

# Сохранение карты
m.save("98.html")