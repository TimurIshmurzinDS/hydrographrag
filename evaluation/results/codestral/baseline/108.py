python
        import pandas as pd
        import geopandas as gpd
        from shapely.geometry import Point
        import folium
        from scipy import stats

        # Загрузка данных
        kurty_data = pd.read_csv('kurty_river_data.csv')
        urzhar_data = pd.read_csv('urzhar_river_data.csv')

        # Вычисление среднего значения и стандартного отклонения
        kurty_mean = kurty_data['flow'].mean()
        kurty_std = kurty_data['flow'].std()
        urzhar_mean = urzhar_data['flow'].mean()
        urzhar_std = urzhar_data['flow'].std()

        # Определение порогового значения экологического стресса
        kurty_threshold = kurty_mean + 2 * kurty_std
        urzhar_threshold = urzhar_mean + 2 * urzhar_std

        # Проверка текущих значений уровня стока
        kurty_data['stress'] = kurty_data['flow'].apply(lambda x: 'Yes' if x > kurty_threshold else 'No')
        urzhar_data['stress'] = urzhar_data['flow'].apply(lambda x: 'Yes' if x > urzhar_threshold else 'No')

        # Создание GeoDataFrame для визуализации на карте
        kurty_geometry = [Point(xy) for xy in zip(kurty_data['longitude'], kurty_data['latitude'])]
        kurty_geo = gpd.GeoDataFrame(kurty_data, geometry=kurty_geometry)

        urzhar_geometry = [Point(xy) for xy in zip(urzhar_data['longitude'], urzhar_data['latitude'])]
        urzhar_geo = gpd.GeoDataFrame(urzhar_data, geometry=urzhar_geometry)

        # Создание карты с использованием библиотеки folium
        m = folium.Map(location=[55, 60], zoom_start=4)

        for idx, row in kurty_geo.iterrows():
            if row['stress'] == 'Yes':
                folium.CircleMarker([row['latitude'], row['longitude']], radius=10, color='red', fill_color='red').add_to(m)
            else:
                folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='green', fill_color='green').add_to(m)

        for idx, row in urzhar_geo.iterrows():
            if row['stress'] == 'Yes':
                folium.CircleMarker([row['latitude'], row['longitude']], radius=10, color='red', fill_color='red').add_to(m)
            else:
                folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='green', fill_color='green').add_to(m)

        # Сохранение карты в файл
        m.save("108.html")