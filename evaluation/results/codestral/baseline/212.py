python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         from sklearn.metrics import mean_squared_error
         import folium

         # Шаг 1: Сбор данных
         bitcoin_data = pd.read_csv('bitcoin_data.csv')
         water_level_data = pd.read_csv('water_level_data.csv')

         # Шаг 2: Очистка данных
         bitcoin_data = bitcoin_data.dropna()
         water_level_data = water_level_data.dropna()

         # Шаг 3: Анализ корреляции
         correlation = bitcoin_data['course'].corr(water_level_data['water_level'])
         print('Корреляция между курсом биткоина и уровнем воды:', correlation)

         # Шаг 4: Подготовка данных
         X = bitcoin_data[['course']]
         y = water_level_data['water_level']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

         # Шаг 5: Моделирование
         model = LinearRegression()
         model.fit(X_train, y_train)

         # Шаг 6: Оценка модели
         predictions = model.predict(X_test)
         rmse = mean_squared_error(y_test, predictions, squared=False)
         print('Среднеквадратическая ошибка (RMSE):', rmse)

         # Шаг 7: Визуализация на карте
         m = folium.Map(location=[55.751244, 37.618423], zoom_start=10)
         for index, row in water_level_data.iterrows():
             folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=row['water_level']*5, color='blue', fill=True, fill_color='blue').add_to(m)
         m.save("212.html")