python
         import pandas as pd
         import folium
         # Загрузка данных
         data = pd.read_csv('housing_data.csv')
         # Анализ данных
         data['cost_difference'] = data['current_cost'] - data['past_cost']
         # Создание карты
         m = folium.Map(location=[55, 37], zoom_start=4)
         # Добавление данных на карту
         for i in range(0, len(data)):
             folium.CircleMarker(
                 location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                 radius=10,
                 color='red' if data.iloc[i]['cost_difference'] > 0 else 'green',
                 fill_color='red' if data.iloc[i]['cost_difference'] > 0 else 'green',
                 popup=data.iloc[i]['city'] + '<br>' + str(data.iloc[i]['cost_difference'])
             ).add_to(m)
         # Сохранение карты
         m.save("280.html")