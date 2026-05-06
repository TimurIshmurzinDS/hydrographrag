python
        import pandas as pd
        import numpy as np
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LinearRegression
        from sklearn import metrics
        import folium

        # Шаг 1: Загрузка данных
        data = pd.read_csv('karkara_river_data.csv')

        # Шаг 2: Предварительный анализ данных
        data = data.dropna()

        # Шаг 3: Исследование связи между осадками и уровнем воды
        correlation = data['precipitation'].corr(data['water_level'])

        # Шаг 4: Моделирование влияния осадков на уровень воды
        X = data['precipitation'].values.reshape(-1,1)
        y = data['water_level'].values.reshape(-1,1)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        regressor = LinearRegression()
        regressor.fit(X_train, y_train)

        # Шаг 5: Оценка модели
        y_pred = regressor.predict(X_test)

        print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
        print('R-squared:', metrics.r2_score(y_test, y_pred))

        # Шаг 6: Визуализация результатов на карте
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

        for i in range(len(data)):
            folium.CircleMarker([data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                                radius=data.iloc[i]['water_level']*5,
                                color='blue',
                                fill=True,
                                fill_color='blue').add_to(m)
        m.save("60.html")