python
         import geopandas as gpd
         import folium
         from shapely.geometry import Point, LineString

         # Загрузка данных о реке
         river = gpd.read_file('river_data.shp')
         current_discharge = 1000  # Текущий расход в кубических метрах в секунду

         # Определение зон риска наводнения (простой пример)
         def calculate_risk(discharge):
             if discharge < 500:
                 return 'Low'
             elif discharge < 1500:
                 return 'Medium'
             else:
                 return 'High'

         river['Risk'] = river.apply(lambda row: calculate_risk(current_discharge), axis=1)

         # Создание индекса риска наводнения (простой пример)
         def risk_index(risk):
             if risk == 'Low':
                 return 1
             elif risk == 'Medium':
                 return 2
             else:
                 return 3

         river['Risk Index'] = river.apply(lambda row: risk_index(row['Risk']), axis=1)

         # Визуализация на карте с помощью folium
         m = folium.Map(location=[river.geometry.centroid.y.mean(), river.geometry.centroid.x.mean()], zoom_start=10)

         for _, r in river.iterrows():
             if r['Risk'] == 'Low':
                 color = 'green'
             elif r['Risk'] == 'Medium':
                 color = 'yellow'
             else:
                 color = 'red'

             folium.PolyLine(locations=[(i.xy[1][0], i.xy[0][0]) for i in r.geometry.coords], color=color).add_to(m)

         m.save("30.html")