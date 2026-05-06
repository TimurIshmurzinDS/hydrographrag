python
         # Импортируем необходимые библиотеки
         import pandas as pd
         import folium

         # Загружаем данные о сезонных паводках для реки Bayankol River
         data = pd.read_csv('bayankol_river_flood_data.csv')

         # Очищаем и преобразуем данные
         # (Этот шаг может включать в себя различные операции, такие как удаление пропущенных значений, изменение типов данных и т.д.)

         # Создаем карту с центром на реки Bayankol River
         m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

         # Добавляем предупреждения о сезонных паводках на карту
         for i in range(len(data)):
             folium.CircleMarker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                                 radius=5,
                                 color='red',
                                 fill_color='red',
                                 popup=f"Warning: {data.iloc[i]['warning']}").add_to(m)

         # Сохраняем карту как "18.html"
         m.save("18.html")