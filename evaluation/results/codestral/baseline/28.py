python
        import folium
        import pandas as pd

        # Загрузка данных (предполагается, что у вас есть доступ к файлу или API)
        data = pd.read_csv('shyzhyn_river_water_level_alerts.csv')

        # Создание карты с базовыми слоями
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

        # Добавление оповещений на карту
        for i in range(len(data)):
            folium.CircleMarker(
                location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                radius=10,
                color='red',
                fill=True,
                fill_color='red'
            ).add_to(m)

        # Сохранение карты
        m.save("28.html")