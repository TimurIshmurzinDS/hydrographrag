python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         from sklearn.metrics import mean_squared_error
         import folium

         # Шаг 1: Загрузка данных
         data = pd.read_csv('trading_strategies.csv')

         # Шаг 2: Очистка и преобразование данных
         data = data.dropna()
         data = (data - data.mean()) / data.std()

         # Шаг 3: Разделение на обучающий и тестовый наборы
         X_train, X_test, y_train, y_test = train_test_split(data.drop('return', axis=1), data['return'], test_size=0.2)

         # Шаг 4: Применение модели машинного обучения
         model = LinearRegression()
         model.fit(X_train, y_train)

         # Шаг 5: Оценка модели
         predictions = model.predict(X_test)
         mse = mean_squared_error(y_test, predictions)

         # Шаг 6: Визуализация на карте
         m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)
         for index, row in data.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']], radius=row['return']*10, color='red').add_to(m)
         m.save("285.html")