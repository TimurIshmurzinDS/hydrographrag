python
         import geopandas as gpd
         import folium

         # Загрузка данных
         tentek_data = gpd.read_file('tentek_river.geojson')
         sharyn_data = gpd.read_file('sharyn_river.geojson')

         # Проверка данных
         print(tentek_data.isnull().sum())
         print(sharyn_data.isnull().sum())

         # Анализ данных (пример: сравнение среднего уровня воды)
         tentek_avg_water_level = tentek_data['water_level'].mean()
         sharyn_avg_water_level = sharyn_data['water_level'].mean()

         print(f'Средний уровень воды в Tentek River: {tentek_avg_water_level}')
         print(f'Средний уровень воды в Sharyn River: {sharyn_avg_water_level}')

         # Визуализация на карте
         m = folium.Map(location=[55, 37], zoom_start=6)

         folium.GeoJson(tentek_data).add_to(m)
         folium.GeoJson(sharyn_data).add_to(m)

         m.save("75.html")