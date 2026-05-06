python
         import geopandas as gpd
         from pykrige.ok import OrdinaryKriging
         import folium
         import numpy as np

         # Загрузка данных о распространении агрокультур и качестве воды
         agro_data = gpd.read_file('agriculture_data.shp')
         water_quality_data = gpd.read_file('water_quality_data.shp')

         # Создание сетки для прогнозирования
         xmin, ymin, xmax, ymax = agro_data.total_bounds
         grid = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]

         # ПрименениеOrdinary Kriging для прогнозирования уровня влияния агрокультуры на качество воды
         OK = OrdinaryKriging(agro_data['geometry'].x, agro_data['geometry'].y, agro_data['impact'], variogram_model='linear', verbose=False)
         z, ss = OK.execute('points', grid[0].ravel(), grid[1].ravel())

         # Создание GeoDataFrame для визуализации результатов
         results = gpd.GeoDataFrame(geometry=[Point(x, y) for x, y in zip(grid[0].ravel(), grid[1].ravel())])
         results['impact'] = z

         # Визуализация результатов на карте с использованием библиотеки folium
         m = folium.Map(location=[agro_data['geometry'].y.mean(), agro_data['geometry'].x.mean()], zoom_start=10)
         m.choropleth(geo_data=results, data=results, columns=['index', 'impact'], key_on='feature.id', fill_color='YlGnBu', legend_name="Уровень влияния агрокультуры на качество воды")
         m.save("42.html")