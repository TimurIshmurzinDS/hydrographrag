python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.ensemble import RandomForestRegressor
         from sklearn.metrics import mean_squared_error
         import folium

         # Шаг 1: Загрузка данных
         data = pd.read_csv('aksurover_data.csv')

         # Шаг 2: Очистка и преобразование данных
         # Здесь могут быть дополнительные шаги в зависимости от конкретных данных
         data = data.dropna()

         # Шаг 3: Разработка модели
         X = data[['precipitation', 'temperature']]  # и другие факторы, если они есть
         y = data['peak_flood']

         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

         model = RandomForestRegressor()
         model.fit(X_train, y_train)

         # Шаг 4: Оценка модели
         predictions = model.predict(X_test)
         mse = mean_squared_error(y_test, predictions)
         print('Mean Squared Error:', mse)

         # Шаг 5: Прогнозирование на следующий сезон
         next_season_data = pd.read_csv('next_season_data.csv')
         next_season_predictions = model.predict(next_season_data[['precipitation', 'temperature']])

         # Шаг 6: Визуализация на карте
         m = folium.Map(location=[41, 75], zoom_start=6)

         for i in range(len(next_season_data)):
             folium.CircleMarker(
                 location=[next_season_data['latitude'].iloc[i], next_season_data['longitude'].iloc[i]],
                 radius=next_season_predictions[i]*0.1,  # умножаем на коэффициент для лучшей визуализации
                 color='red',
                 fill=True,
                 fill_color='red'
             ).add_to(m)

         m.save("197.html")