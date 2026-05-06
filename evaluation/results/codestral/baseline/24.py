python
         # Импортируем необходимые библиотеки
         import pandas as pd
         import folium

         # Загружаем данные
         data = pd.read_csv('ulken_almaty_river_floods.csv')

         # Очищаем и преобразуем данные
         # (здесь могут быть дополнительные шаги в зависимости от структуры ваших данных)
         data = data[data['season'] == 'spring']

         # Создаем карту
         m = folium.Map(location=[43.25, 76.95], zoom_start=10)

         # Добавляем данные на карту
         for i in range(len(data)):
             folium.CircleMarker(
                 location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                 radius=5,
                 color='red',
                 fill=True,
                 fill_color='red'
             ).add_to(m)

         # Сохраняем карту
         m.save("24.html")