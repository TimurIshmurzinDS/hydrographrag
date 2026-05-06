python
         import pandas as pd
         import folium
         from sklearn.linear_model import LinearRegression

         # Шаг 1: Загрузка данных
         land_data = pd.read_csv('land_data.csv')
         climate_data = pd.read_csv('climate_data.csv')

         # Шаг 2 и 3: Анализ данных
         merged_data = pd.merge(land_data, climate_data, on='date')
         X = merged_data[['temperature', 'precipitation', 'sunlight']]
         y = merged_data['ecological_stability']
         model = LinearRegression().fit(X, y)

         # Шаг 4: Оценка экологической устойчивости в контексте изменения климата
         future_climate_data = pd.read_csv('future_climate_data.csv')
         future_ecological_stability = model.predict(future_climate_data[['temperature', 'precipitation', 'sunlight']])

         # Шаг 5: Визуализация результатов на карте
         m = folium.Map(location=[land_data['lat'].mean(), land_data['lon'].mean()], zoom_start=10)
         for i in range(len(land_data)):
             folium.CircleMarker([land_data.iloc[i]['lat'], land_data.iloc[i]['lon']],
                                 radius=5,
                                 color='green' if future_ecological_stability[i] > merged_data['ecological_stability'].mean() else 'red').add_to(m)
         m.save("184.html")