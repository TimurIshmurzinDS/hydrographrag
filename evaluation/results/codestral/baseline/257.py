python
         import pandas as pd
         import geopandas as gpd
         from shapely.geometry import Point
         import folium
         # Загрузка данных о уровне воды в реке Баянколь
         water_level = pd.read_csv('water_level.csv')
         # Загрузка геоданных о сельскохозяйственных землях
         land = gpd.read_file('land.shp')
         # Функция для расчета потребности в поливе на основе уровня воды в реке
         def calculate_irrigation(water_level):
             if water_level < 10:
                 return 'High'
             elif water_level < 20:
                 return 'Medium'
             else:
                 return 'Low'
         # Применение функции к каждому участку земли
         land['irrigation'] = land.apply(lambda row: calculate_irrigation(water_level.iloc[-1]['level']), axis=1)
         # Визуализация результатов на карте с помощью библиотеки folium
         m = folium.Map(location=[land.geometry.centroid.y.mean(), land.geometry.centroid.x.mean()], zoom_start=10)
         for _, r in land.iterrows():
             folium.GeoJson(r['geometry'].__geo_interface__, style_function=lambda x: {'fillColor': 'red' if x['properties']['irrigation'] == 'High' else 'yellow' if x['properties']['irrigation'] == 'Medium' else 'green'}).add_to(m)
         m.save("257.html")