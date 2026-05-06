python
        # Импортирование необходимых библиотек
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        import folium

        # Загрузка данных
        dos_data = pd.read_csv('dos_river_data.csv')
        lepsy_data = pd.read_csv('lepsy_river_data.csv')

        # Очистка и преобразование данных (этот шаг может быть необходим в зависимости от ваших данных)
        dos_data['date'] = pd.to_datetime(dos_data['date'])
        lepsy_data['date'] = pd.to_datetime(lepsy_data['date'])

        # Создание модели
        X = dos_data[['water_level', 'rainfall', 'temperature']]  # и другие релевантные признаки
        y = lepsy_data['water_level']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        # Прогнозирование уровня воды в реке Lepsy River на 2025 год
        future_data = pd.DataFrame({'date': pd.date_range(start='2024-12-31', end='2025-12-31'),
                                    'water_level': [dos_data['water_level'].mean()] * 365,
                                    'rainfall': [dos_data['rainfall'].mean()] * 365,
                                    'temperature': [dos_data['temperature'].mean()] * 365})
        future_predictions = model.predict(future_data[['water_level', 'rainfall', 'temperature']])

        # Визуализация результатов на карте
        m = folium.Map(location=[lepsy_data['latitude'].mean(), lepsy_data['longitude'].mean()], zoom_start=10)

        for i in range(len(future_predictions)):
            folium.CircleMarker(
                location=[lepsy_data['latitude'].iloc[i % len(lepsy_data)], lepsy_data['longitude'].iloc[i % len(lepsy_data)]],
                radius=future_predictions[i] / 10,
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

        m.save("124.html")