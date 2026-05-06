import geopandas as gpd
from shapely import wkt

# Загрузите shapefile с использованием raw string и преобразуйте его в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине shapefile и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте область бассейна на карту с помощью GeoJson
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создайте список словарей для координат точек (WKT)
wkt_coords = [
    {'type': 'Point', 'coordinates': [55.123, 37.456]},
    {'type': 'Point', 'coordinates': [56.789, 38.901]}
]

# Добавьте точки на карту
for coord in wkt_coords:
    folium.Marker(location=coord['coordinates'], popup='Точка').add_to(m)

# Рассчитайте год с самым высоким уровнем стока в реке Lepsy River и сравните его с аналогичным периодом в реке Tekes River
max_year = max(gdf[gdf['name'] == 'Lepsy River']['Date_water_level_Value'])
min_year = min(gdf[gdf['name'] == 'Tekes River']['Date_water_level_Value'])

# Сравните результаты
if max_year > min_year:
    print('Река Lepsy River имеет самый высокий уровень стока в году', max_year)
else:
    print('Река Tekes River имеет самый высокий уровень стока в году', min_year)

# Сохраните карту с использованием строки filename
m.save("132.html")