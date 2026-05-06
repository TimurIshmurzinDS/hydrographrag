python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         from sklearn.metrics import mean_squared_error
         import folium

         # Шаг 1: Подготовка данных
         river_data = pd.read_csv('bayankol_river_data.csv')
         bitcoin_data = pd.read_csv('bitcoin_price_data.csv')
         data = pd.merge(river_data, bitcoin_data, on='date')

         # Шаг 2: Анализ данных
         correlation = data['water_level'].corr(data['bitcoin_price'])
         print('Correlation between water level and Bitcoin price:', correlation)

         # Шаг 3: Построение модели
         X = data[['water_level']]
         y = data['bitcoin_price']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
         model = LinearRegression()
         model.fit(X_train, y_train)

         # Шаг 4: Оценка модели
         predictions = model.predict(X_test)
         mse = mean_squared_error(y_test, predictions)
         print('Mean Squared Error:', mse)

         # Шаг 5: Визуализация результатов
         map_center = [data['latitude'].mean(), data['longitude'].mean()]
         m = folium.Map(location=map_center, zoom_start=10)
         for index, row in data.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
         m.save("271.html")