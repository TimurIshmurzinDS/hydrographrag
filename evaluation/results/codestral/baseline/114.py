python
         import folium
         import pandas as pd
         # Предполагается, что у вас есть DataFrame df с данными о реках
         # df = pd.read_csv('rivers_data.csv')
         # Допустим, что в df есть столбцы 'river', 'flow_rate' (дебит) и 'length' (длина)
         # Расчет ирригационного потенциала
         df['irrigation_potential'] = df['flow_rate'] * df['length']
         # Создание карты
         m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=5)
         # Добавление меток на карту
         for i in range(0,len(df)):
             folium.Marker([df.iloc[i]['lat'], df.iloc[i]['lon']], popup=df.iloc[i]['river'] + ': ' + str(df.iloc[i]['irrigation_potential'])).add_to(m)
         # Сохранение карты
         m.save("114.html")