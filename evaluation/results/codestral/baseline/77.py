python
         import pandas as pd
         from statsmodels.tsa.seasonal import seasonal_decompose
         from scipy import stats
         import folium

         # Загрузка данных
         baskan = pd.read_csv('baskan_river_data.csv')
         prokhodnaya = pd.read_csv('prokhodnaya_river_data.csv')

         # Анализ временных рядов и выделение сезонности
         baskan_seasonal = seasonal_decompose(baskan['discharge'], model='additive', period=12)
         prokhodnaya_seasonal = seasonal_decompose(prokhodnaya['discharge'], model='additive', period=12)

         # Сравнение сезонных уровней расхода
         t_stat, p_value = stats.ttest_ind(baskan_seasonal.seasonal, prokhodnaya_seasonal.seasonal)

         print(f'T-статистика: {t_stat}, p-значение: {p_value}')

         # Прогнозирование (здесь простой пример с использованием среднего значения за последний сезон)
         baskan_spring_avg = baskan[baskan['season'] == 'spring']['discharge'].mean()
         prokhodnaya_spring_avg = prokhodnaya[prokhodnaya['season'] == 'spring']['discharge'].mean()

         # Визуализация на карте (предполагается, что у вас есть координаты рек)
         m = folium.Map(location=[55, 37], zoom_start=6)

         folium.Marker([baskan['lat'].mean(), baskan['lon'].mean()], popup=f'Baskan River: {baskan_spring_avg}').add_to(m)
         folium.Marker([prokhodnaya['lat'].mean(), prokhodnaya['lon'].mean()], popup=f'Prokhodnaya River: {prokhodnaya_spring_avg}').add_to(m)

         m.save("77.html")