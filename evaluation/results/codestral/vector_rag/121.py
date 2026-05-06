python
   # Импортируем необходимые библиотеки
   import geopandas as gpd
   import folium
   from shapely import wkt

   # Загружаем данные о бассейне
   basin = gpd.read_file(r"data/basin_data.shp")
   basin = basin.to_crs('EPSG:4326')

   # Инициализируем карту folium с центром в центроиде бассейна
   m = folium.Map(location=[basin.centroid.y, basin.centroid.x], tiles='CartoDB positron')

   # Добавляем границы бассейна на карту
   folium.GeoJson(basin['geometry'], name='Basin', style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

   # Предположим, что у нас есть данные о расходе воды в реках за последние 10 лет
   bayankol_river_flow = [100, 110, 95, ...]  # Замените на фактические данные
   shilik_river_flow = [80, 90, 75, ...]  # Замените на фактические данные

   # Вычисляем средний расход воды в реках за последние 10 лет
   bayankol_avg_flow = sum(bayankol_river_flow) / len(bayankol_river_flow)
   shilik_avg_flow = sum(shilik_river_flow) / len(shilik_river_flow)

   # Сравниваем средние расходы воды в реках
   if bayankol_avg_flow > shilik_avg_flow:
       print("Средний расход воды в реке Баянкол выше, чем в реке Шилик за последние 10 лет.")
   elif bayankol_avg_flow < shilik_avg_flow:
       print("Средний расход воды в реке Шилик выше, чем в реке Баянкол за последние 10 лет.")
   else:
       print("Средний расход воды в реках Баянкол и Шилик одинаков за последние 10 лет.")

   # Сохраняем карту
   m.save("121.html")