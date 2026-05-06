python
        # Импортируем необходимые библиотеки
        import pandas as pd
        from statsmodels.tsa.arima_model import ARIMA
        import folium

        # Загружаем данные
        data = pd.read_csv('dos_river_water_level.csv')

        # Преобразуем столбец с датами в индекс и устанавливаем его как временной индекс
        data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date', inplace=True)

        # Создаем модель ARIMA
        model = ARIMA(data['Water Level'], order=(5,1,0))
        model_fit = model.fit(disp=0)

        # Прогнозируем будущий уровень воды на 365 дней вперед
        forecast = model_fit.forecast(steps=365)

        # Создаем карту с помощью folium
        m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=10)

        # Добавляем прогноз на карту
        for i in range(len(forecast[0])):
            folium.CircleMarker(
                location=[data['Latitude'].iloc[-1], data['Longitude'].iloc[-1]],
                radius=forecast[0][i]*5, # Умножаем на некоторое число для визуализации
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

        # Сохраняем карту
        m.save("221.html")