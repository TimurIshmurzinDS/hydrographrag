python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         from sklearn.metrics import mean_squared_error
         import folium
         from statsmodels.tsa.seasonal import seasonal_decompose

         # Загрузка данных
         data = pd.read_csv('sharyn_river_data.csv', parse_dates=['Date'], index_col='Date')

         # Анализ временных трендов и сезонности
         decomposition = seasonal_decompose(data['Water Flow'], model='multiplicative')

         # Подготовка данных для моделирования
         data['Month'] = data.index.month
         X = data[['Month']]
         y = data['Water Flow']

         # Разделение на обучающий и тестовый наборы
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

         # Построение прогнозирующей модели
         model = LinearRegression()
         model.fit(X_train, y_train)

         # Прогнозирование и оценка точности модели
         predictions = model.predict(X_test)
         mse = mean_squared_error(y_test, predictions)
         print('Mean Squared Error:', mse)

         # Визуализация прогнозов на карте
         m = folium.Map(location=[43.2567, 76.9286], zoom_start=10)
         for month in range(1, 13):
             prediction = model.predict([[month]])
             folium.CircleMarker(location=[43.2567, 76.9286], radius=prediction/100, color='blue', fill_color='blue').add_to(m)
         m.save("131.html")