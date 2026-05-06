python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.ensemble import RandomForestRegressor
         import folium

         # Шаг 1: Сбор данных
         data = pd.read_csv('sarykan_river_data.csv')

         # Шаг 2: Предобработка данных
         # Здесь могут быть дополнительные шаги в зависимости от конкретных данных
         data = data.dropna()

         # Шаг 3: Разделение данных
         X = data[['precipitation', 'temperature']]  # и другие факторы
         y = data['flow']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

         # Шаг 4: Выбор модели
         model = RandomForestRegressor()

         # Шаг 5: Обучение модели
         model.fit(X_train, y_train)

         # Шаг 6: Проверка производительности модели
         score = model.score(X_test, y_test)
         print('R^2 Score:', score)

         # Шаг 7: Прогнозирование на следующий сезон
         next_season_data = pd.read_csv('next_season_data.csv')
         predictions = model.predict(next_season_data[['precipitation', 'temperature']])

         # Шаг 8: Визуализация результатов на карте
         m = folium.Map(location=[54.98, 73.32], zoom_start=10)
         for i in range(len(predictions)):
             folium.Marker([next_season_data['latitude'][i], next_season_data['longitude'][i]], popup=str(predictions[i])).add_to(m)
         m.save("52.html")