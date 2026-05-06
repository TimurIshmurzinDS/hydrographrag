python
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import r2_score, mean_absolute_error
        import folium

        # Шаг 1: Загрузка данных
        data = pd.read_csv('real_estate_data.csv')

        # Шаг 2: Предварительный анализ данных
        print(data.describe())
        print(data.isnull().sum())

        # Шаг 3: Кодирование категориальных переменных (если необходимо)
        data = pd.get_dummies(data, drop_first=True)

        # Шаг 4: Разделение данных на обучающий и тестовый наборы
        X = data.drop('price', axis=1)
        y = data['price']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Шаг 5: Создание модели регрессии
        model = LinearRegression()

        # Шаг 6: Обучение модели и оценка производительности
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        print('R-squared:', r2_score(y_test, predictions))
        print('Mean Absolute Error:', mean_absolute_error(y_test, predictions))

        # Шаг 7: Предсказание цен на недвижимость в тестовом наборе данных
        data['predicted_price'] = model.predict(X)

        # Шаг 8: Визуализация результатов на карте с помощью библиотеки folium
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)
        for index, row in data.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
        m.save("279.html")