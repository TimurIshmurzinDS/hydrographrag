python
         import pandas as pd
         import matplotlib.pyplot as plt
         from scipy import stats
         import folium

         # Загрузка данных
         ili_data = pd.read_csv('ili_river_data.csv')
         shyzhyn_data = pd.read_csv('shyzhyn_river_data.csv')

         # Проверка данных на пропуски и аномалии
         ili_data = ili_data.dropna()
         shyzhyn_data = shyzhyn_data.dropna()

         # Сравнение уровней сезонного расхода воды
         t_stat, p_value = stats.ttest_ind(ili_data['seasonal_flow'], shyzhyn_data['seasonal_flow'])

         print(f'T-статистика: {t_stat}, p-значение: {p_value}')

         # Визуализация на карте
         m = folium.Map(location=[51, 71], zoom_start=4)

         ili_avg_flow = ili_data['seasonal_flow'].mean()
         shyzhyn_avg_flow = shyzhyn_data['seasonal_flow'].mean()

         folium.Marker(location=[52, 71], popup=f'Ili River Average Flow: {ili_avg_flow}').add_to(m)
         folium.Marker(location=[49, 73], popup=f'Shyzhyn River Average Flow: {shyzhyn_avg_flow}').add_to(m)

         m.save("160.html")