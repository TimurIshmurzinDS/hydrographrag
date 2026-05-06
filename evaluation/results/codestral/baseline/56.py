python
        # Импортируем необходимые библиотеки
        import pandas as pd
        import matplotlib.pyplot as plt
        import folium

        # Загружаем данные
        data = pd.read_csv('dos_river_sedimentation_data.csv')

        # Группируем данные по годам и суммируем наносы
        annual_load = data.groupby(pd.DatetimeIndex(data['date']).year)['sedimentation'].sum()

        # Визуализируем данные с помощью графика
        plt.figure(figsize=(10, 6))
        plt.plot(annual_load.index, annual_load.values)
        plt.title('Historical Sedimentation Load in Dos River Over the Last 5 Years')
        plt.xlabel('Year')
        plt.ylabel('Sedimentation Load')
        plt.show()

        # Создаем карту с помощью folium
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

        # Добавляем точки на карту, представляющие местоположения наносов
        for i in range(len(data)):
            folium.CircleMarker([data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                                radius=data.iloc[i]['sedimentation']/100, # Размер точки пропорционален нагрузке наносов
                                color='blue',
                                fill_color='blue').add_to(m)

        # Сохраняем карту
        m.save("56.html")