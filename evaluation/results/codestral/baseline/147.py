python
         import pandas as pd
         import folium

         # 1. Загрузка данных
         data = pd.read_csv('sensor_data.csv')

         # 2. Проверка на пропущенные значения
         missing_values = data.isnull().sum()

         # 3. Определение ошибок в данных (пример: значения меньше 0 или больше 100)
         errors = data[(data['sensor_value'] < 0) | (data['sensor_value'] > 100)]

         # 4. Визуализация результатов на карте
         m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

         for index, row in errors.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='red').add_to(m)

         m.save("147.html")