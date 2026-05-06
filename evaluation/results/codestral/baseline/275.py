python
         import pandas as pd
         from sklearn.model_selection import train_test_split
         from sklearn.ensemble import RandomForestClassifier
         import folium

         # Шаг 1: Загрузка данных
         data = pd.read_csv('solar_flare_data.csv')

         # Шаг 2: Очистка и преобразование данных
         # (Этот шаг может включать в себя различные методы, такие как заполнение пропущенных значений, кодирование категориальных переменных и т.д.)

         # Шаг 3: Создание модели машинного обучения
         X = data[['feature1', 'feature2', 'feature3']]  # Замените на фактические признаки
         y = data['flare_probability']

         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

         model = RandomForestClassifier()
         model.fit(X_train, y_train)

         # Шаг 4: Визуализация результатов на карте
         m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2)

         for index, row in data.iterrows():
             folium.CircleMarker([row['latitude'], row['longitude']],
                                 radius=row['flare_probability']*5,  # Умножаем на число для увеличения размера точек
                                 color='red',
                                 fill=True,
                                 fill_color='red').add_to(m)

         m.save("275.html")