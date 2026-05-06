python
         import pandas as pd
         import folium
         from matplotlib import pyplot as plt
         from scipy import stats
         # Загрузка данных
         tekes_data = pd.read_csv('tekes_river_data.csv')
         bayankol_data = pd.read_csv('bayankol_river_data.csv')
         # Проверка данных
         print(tekes_data.isnull().sum())
         print(bayankol_data.isnull().sum())
         # Визуализация на карте
         m = folium.Map()
         for index, row in tekes_data.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']], radius=row['discharge']/100, color='blue').add_to(m)
         for index, row in bayankol_data.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']], radius=row['discharge']/100, color='red').add_to(m)
         m.save("25.html")
         # Сравнение уровней расхода воды
         plt.figure(figsize=(10, 6))
         plt.plot(tekes_data['date'], tekes_data['discharge'], label='Tekes River')
         plt.plot(bayankol_data['date'], bayankol_data['discharge'], label='Bayankol River')
         plt.legend()
         plt.show()
         # Статистический тест (например, t-test)
         t_statistic, p_value = stats.ttest_ind(tekes_data['discharge'], bayankol_data['discharge'])
         print('T-Statistic:', t_statistic)
         print('P-Value:', p_value)