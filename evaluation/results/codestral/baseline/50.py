python
        # Импорт необходимых библиотек
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.metrics import mean_absolute_error, r2_score
        import folium

        # Загрузка данных
        data = pd.read_csv('dos_river_data.csv')

        # Предобработка данных
        data = data.dropna()  # Удаление пропущенных значений
        data = (data - data.mean()) / data.std()  # Нормализация данных

        # Выбор признаков и целевой переменной
        features = ['precipitation', 'temperature', 'humidity']
        target = 'water_level'

        X = data[features]
        y = data[target]

        # Разделение данных на обучающий и тестовый наборы
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Выбор модели и ее обучение
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Оценка модели
        predictions = model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        print(f'MAE: {mae}, R²: {r2}')

        # Прогнозирование на новых данных
        new_data = pd.DataFrame({
            'precipitation': [0.5],
            'temperature': [15],
            'humidity': [60]
        })
        predicted_water_level = model.predict(new_data)
        print(f'Predicted water level: {predicted_water_level[0]}')

        # Визуализация на карте с помощью folium
        m = folium.Map(location=[latitude, longitude], zoom_start=12)
        folium.Marker([latitude, longitude], popup=f'Predicted water level: {predicted_water_level[0]}').add_to(m)
        m.save("50.html")