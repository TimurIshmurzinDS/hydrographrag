python
       import geopandas as gpd
       import folium
       from shapely import wkt

       # Загрузка данных о реке Кумбель из файла (предположительно в формате GeoJSON или CSV)
       # В этом примере используется GeoJSON, но код может быть адаптирован под другие форматы
       gdf = gpd.read_file('data/kumbel_river_data.geojson')

       # Преобразование системы координат в 'EPSG:4326'
       gdf = gdf.to_crs(epsg=4326)

       # Инициализация карты folium с центром на реке Кумбель
       m = folium.Map(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], tiles='CartoDB positron')

       # Добавление данных о реке Кумбель на карту
       folium.GeoJson(gdf, name='Kumbel River').add_to(m)

       # Сортировка данных по дате измерений в убывающем порядке и выбор последнего значения уровня воды
       latest_water_level = gdf.sort_values('Date_water_level_Value').iloc[-1]['Water_level_Value']

       # Вывод последнего значения уровня воды на карту (в этом примере используется маркер)
       folium.Marker(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], popup=f'Last water level: {latest_water_level}').add_to(m)

       # Сохранение карты в файл
       m.save("13.html")