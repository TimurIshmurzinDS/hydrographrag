python
         import pandas as pd
         import numpy as np
         from scipy import stats
         import folium

         # Шаг 1: Загрузка данных
         precipitation_data = pd.read_csv('precipitation_data.csv')
         flow_data_urzhar = pd.read_csv('flow_data_urzhar.csv')
         flow_data_byzhy = pd.read_csv('flow_data_byzhy.csv')

         # Шаг 2: Очистка и преобразование данных
         precipitation_data['date'] = pd.to_datetime(precipitation_data['date'])
         flow_data_urzhar['date'] = pd.to_datetime(flow_data_urzhar['date'])
         flow_data_byzhy['date'] = pd.to_datetime(flow_data_byzhy['date'])

         # Объединение данных по дате
         merged_data_urzhar = pd.merge(precipitation_data, flow_data_urzhar, on='date')
         merged_data_byzhy = pd.merge(precipitation_data, flow_data_byzhy, on='date')

         # Шаг 3: Оценка корреляции
         correlation_urzhar, _ = stats.pearsonr(merged_data_urzhar['precipitation'], merged_data_urzhar['flow'])
         correlation_byzhy, _ = stats.pearsonr(merged_data_byzhy['precipitation'], merged_data_byzhy['flow'])

         print('Корреляция Уржар: %.3f' % correlation_urzhar)
         print('Корреляция Быжь: %.3f' % correlation_byzhy)

         # Шаг 4: Визуализация на карте (предполагается, что есть данные о координатах рек)
         m = folium.Map(location=[55.751244, 37.618423], zoom_start=10)

         # Добавление маркеров на карту (замените координаты на реальные)
         folium.Marker([55.751244, 37.618423], popup='Уржар: Корреляция %.3f' % correlation_urzhar).add_to(m)
         folium.Marker([55.751244, 37.619423], popup='Быжь: Корреляция %.3f' % correlation_byzhy).add_to(m)

         m.save("199.html")