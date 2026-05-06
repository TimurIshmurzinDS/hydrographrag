python
         import pandas as pd
         from scipy import stats
         import folium
         from pykrige.ok import OrdinaryKriging

         # Шаг 1: Сбор данных
         data = pd.read_csv('mars_climate_data.csv')

         # Шаг 2: Очистка и предобработка данных
         data = data.dropna()

         # Шаг 3: Статистический анализ
         trend = stats.linregress(data['year'], data['temperature'])

         # Шаг 4: Геостатистический анализ
         OK = OrdinaryKriging(data['longitude'], data['latitude'], data['temperature'], variogram_model='linear', verbose=False)
         z, ss = OK.execute('points', data['longitude'], data['latitude'])

         # Шаг 5: Визуализация на карте
         m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=3)
         for i in range(len(data)):
             folium.CircleMarker([data['latitude'][i], data['longitude'][i]], radius=5, color='red', fill=True, fill_color='red').add_to(m)
         m.save("284.html")