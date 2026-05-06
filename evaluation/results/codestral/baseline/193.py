python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.linear_model import LinearRegression
         import folium

         # Шаг 1: Загрузка данных
         data = pd.read_csv('tokyraun_data.csv')

         # Шаг 2: Очистка и преобразование данных
         # (Этот шаг может включать в себя различные операции, такие как заполнение пропущенных значений, удаление выбросов и т.д.)

         # Шаг 3: Анализ данных
         correlation = data['discharge'].corr(data['irrigation_demand'])

         # Шаг 4: Разработка прогнозирующей модели
         X = data[['discharge']]
         y = data['irrigation_demand']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
         model = LinearRegression()
         model.fit(X_train, y_train)

         # Шаг 5: Прогнозирование будущей потребности в воде для орошения
         future_discharge = pd.DataFrame({'discharge': [100, 200, 300]})  # Примерные данные
         predicted_demand = model.predict(future_discharge)

         # Шаг 6: Визуализация результатов на карте
         m = folium.Map(location=[55.75, 37.61], zoom_start=10)
         for i in range(len(predicted_demand)):
             folium.Marker([55.75 + i*0.1, 37.61 + i*0.1], popup='Predicted demand: ' + str(predicted_demand[i])).add_to(m)
         m.save("193.html")