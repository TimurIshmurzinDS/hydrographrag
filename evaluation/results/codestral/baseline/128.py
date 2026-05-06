python
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn import metrics
        import folium

        # Загрузка данных
        lepsy_data = pd.read_csv('lepsy_river_data.csv')
        dos_data = pd.read_csv('dos_river_data.csv')

        # Очистка и преобразование данных
        # ... (здесь могут быть шаги по очистке и преобразованию данных)

        # Создание корреляционной матрицы
        correlation = lepsy_data['water_level'].corr(dos_data['flood_occurrence'])

        # Создание прогнозирующей модели
        X = lepsy_data['water_level'].values.reshape(-1,1)
        y = dos_data['flood_occurrence']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        # Предсказание вероятности паводки на следующий сезон
        next_season_water_level = pd.read_csv('next_season_lepsy_river_data.csv')['water_level']
        flood_probability = regressor.predict(next_season_water_level.values.reshape(-1,1))

        # Визуализация результатов на карте
        m = folium.Map(location=[dos_river_latitude, dos_river_longitude], zoom_start=10)
        folium.Marker([dos_river_latitude, dos_river_longitude], popup=f'Flood Probability: {flood_probability[0]}').add_to(m)
        m.save("128.html")