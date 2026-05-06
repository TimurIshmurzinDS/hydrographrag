python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.metrics import mean_absolute_error, r2_score
         from historical_weather_forecasting import HistoricalMethod  # Предполагается наличие собственного модуля для исторических методов прогнозирования погоды
         from modern_weather_forecasting import ModernAlgorithm  # Предполагается наличие собственного модуля для современных алгоритмов прогнозирования погоды
         import folium

         # Шаг 1: Собрать данные
         data = pd.read_csv('weather_data.csv')

         # Шаг 2: Разбить данные на обучающий и тестовый наборы
         train_data, test_data = train_test_split(data, test_size=0.2)

         # Шаг 3: Применить исторические методы прогнозирования погоды
         historical_method = HistoricalMethod()
         historical_predictions = historical_method.predict(train_data)
         historical_mae = mean_absolute_error(test_data['temperature'], historical_predictions)
         historical_r2 = r2_score(test_data['temperature'], historical_predictions)

         # Шаг 4: Применить современные алгоритмы прогнозирования погоды
         modern_algorithm = ModernAlgorithm()
         modern_predictions = modern_algorithm.predict(train_data)
         modern_mae = mean_absolute_error(test_data['temperature'], modern_predictions)
         modern_r2 = r2_score(test_data['temperature'], modern_predictions)

         # Шаг 6: Визуализировать результаты на карте с использованием библиотеки `folium`
         m = folium.Map(location=[55.75, 37.62], zoom_start=10)
         for index, row in test_data.iterrows():
             folium.Marker([row['latitude'], row['longitude']], popup=f"Historical: {historical_predictions[index]}, Modern: {modern_predictions[index]}").add_to(m)
         m.save("281.html")