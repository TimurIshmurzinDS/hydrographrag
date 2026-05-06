python
        import pandas as pd
        from statsmodels.tsa.arima_model import ARIMA
        from sklearn.metrics import mean_squared_error
        import folium
        from folium.plugins import MarkerCluster

        # Шаг 1: Собрать данные
        data = pd.read_csv('shyzhyn_river_data.csv', index_col='Date', parse_dates=True)

        # Шаг 2: Проверить тренды и паттерны (здесь пропущено для краткости)

        # Шаг 3: Разбить данные на обучающий и тестовый наборы
        train_data = data[:-365]
        test_data = data[-365:]

        # Шаг 4: Использовать модель ARIMA для прогнозирования
        model = ARIMA(train_data, order=(5,1,0))
        fitted_model = model.fit(disp=0)
        predictions = fitted_model.predict(start=len(train_data), end=len(train_data)+len(test_data)-1)

        # Шаг 5: Оценить точность модели
        mse = mean_squared_error(test_data, predictions)
        print('Mean Squared Error of predictions is {}'.format(mse))

        # Шаг 6: Визуализировать прогнозы на карте
        m = folium.Map(location=[50.4501, 30.5234], zoom_start=10) # Координаты реки Шижин
        marker_cluster = MarkerCluster().add_to(m)
        for i in range(len(predictions)):
            folium.Marker([50.4501, 30.5234], popup=f'Predicted Flow: {predictions[i]}').add_to(marker_cluster)
        m.save("21.html")