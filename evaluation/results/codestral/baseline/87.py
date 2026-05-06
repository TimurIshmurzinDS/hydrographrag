python
        import pandas as pd
        import folium
        from scipy import stats

        # Шаг 1: Загрузка исторических данных
        historical_data = pd.read_csv('historical_data.csv')
        historical_data['datetime'] = pd.to_datetime(historical_data['datetime'])

        # Шаг 2: Очистка и преобразование текущих данных
        current_data = pd.read_csv('current_data.csv')
        current_data['datetime'] = pd.to_datetime(current_data['datetime'])

        # Шаг 3: Сравнение текущего расхода с историческими данными
        spring_flood_data = historical_data[historical_data['datetime'].dt.month == 3]  # Предполагается, что весна - это март
        z_scores = stats.zscore(spring_flood_data['discharge'])
        threshold = 2  # Пороговое значение для определения аномалий (может быть настроено)
        spring_flood_anomalies = spring_flood_data[abs(z_scores) > threshold]

        # Шаг 4: Визуализация результатов на карте
        m = folium.Map(location=[55.75, 37.62], zoom_start=10)  # Пример координат для Москвы

        for _, row in spring_flood_anomalies.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                color='red',
                fill=True,
                fill_color='red'
            ).add_to(m)

        for _, row in current_data.iterrows():
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=3,
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

        m.save("87.html")