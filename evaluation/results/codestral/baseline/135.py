python
         import pandas as pd
         import folium
         from scipy import stats

         # Загрузка данных
         shilik_data = pd.read_csv('shilik_drought_data.csv')
         sharyn_data = pd.read_csv('sharyn_drought_data.csv')

         # Очистка и преобразование данных
         def clean_data(df):
             df['date'] = pd.to_datetime(df['date'])
             df['year'] = df['date'].dt.year
             return df

         shilik_data = clean_data(shilik_data)
         sharyn_data = clean_data(sharyn_data)

         # Сравнение интенсивности летней засухи
         def compare_droughts(df1, df2):
             t_statistic, p_value = stats.ttest_ind(df1['severity'], df2['severity'])
             return t_statistic, p_value

         t_statistic, p_value = compare_droughts(shilik_data, sharyn_data)
         print(f'T-Statistic: {t_statistic}, P-Value: {p_value}')

         # Визуализация на карте
         m = folium.Map(location=[51.2, 71.4], zoom_start=6)

         shilik_layer = folium.FeatureGroup(name='Shilik River Drought Severity')
         for index, row in shilik_data.iterrows():
             folium.CircleMarker([row['lat'], row['lon']], radius=row['severity'], color='red').add_to(shilik_layer)

         sharyn_layer = folium.FeatureGroup(name='Sharyn River Drought Severity')
         for index, row in sharyn_data.iterrows():
             folium.CircleMarker([row['lat'], row['lon']], radius=row['severity'], color='blue').add_to(sharyn_layer)

         m.add_child(shilik_layer)
         m.add_child(sharyn_layer)
         folium.LayerControl().add_to(m)

         # Сохранение карты
         m.save("135.html")