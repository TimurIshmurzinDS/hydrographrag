python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         import folium
         from folium.plugins import HeatMap

         # Шаг 1: Сбор данных
         data = pd.read_csv('crypto_data.csv')

         # Шаг 2: Очистка и преобразование данных
         data['date'] = pd.to_datetime(data['date'])
         data['volatility'] = data['high'] - data['low']
         data = data[['date', 'price', 'volatility']]

         # Шаг 3: Разделение данных
         X = data[['volatility']]
         y = data['price']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

         # Шаг 4: Моделирование
         model = LinearRegression()
         model.fit(X_train, y_train)
         predictions = model.predict(X_test)

         # Шаг 5: Оценка точности и визуализация на карте
         m = folium.Map(location=[0, 0], zoom_start=2)
         heat_data = [[row['lat'], row['lon'], row['predicted_price']] for index, row in data.iterrows()]
         HeatMap(heat_data).add_to(m)
         m.save("282.html")