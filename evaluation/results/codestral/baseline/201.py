python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.ensemble import RandomForestRegressor
         import folium

         # Шаг 1: Сбор данных
         data = pd.read_csv('historical_data.csv')

         # Шаг 2: Предобработка данных
         data = data.dropna()
         data = (data - data.mean()) / data.std()

         # Шаг 3: Выбор модели
         model = RandomForestRegressor(n_estimators=100, random_state=42)

         # Шаг 4: Обучение модели
         X = data.drop('drought_risk', axis=1)
         y = data['drought_risk']
         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
         model.fit(X_train, y_train)

         # Шаг 5: Прогнозирование
         predictions = model.predict(X_test)

         # Шаг 6: Визуализация
         m = folium.Map(location=[42, 71], zoom_start=6)
         folium.Choropleth(geo_data='basin_boundaries.geojson', data=predictions, key_on='feature.id').add_to(m)
         m.save("201.html")