python
        # Импортирование необходимых библиотек
        import pandas as pd
        import geopandas as gpd
        from scipy import stats
        import folium

        # Загрузка данных
        dos_rainfall = pd.read_csv('dos_river_rainfall.csv')
        kurty_flow = pd.read_csv('kurty_river_flow.csv')

        # Преобразование данных в GeoDataFrame
        dos_rainfall = gpd.GeoDataFrame(dos_rainfall, geometry=gpd.points_from_xy(dos_rainfall.longitude, dos_rainfall.latitude))
        kurty_flow = gpd.GeoDataFrame(kurty_flow, geometry=gpd.points_from_xy(kurty_flow.longitude, kurty_flow.latitude))

        # Сравнение влияния недавних осадков на сток реки Dos River относительно исторических данных реки Kurty River
        correlation, p_value = stats.pearsonr(dos_rainfall['rainfall'], kurty_flow['flow'])

        print(f'Корреляция: {correlation}, p-значение: {p_value}')

        # Визуализация на карте с помощью folium
        m = folium.Map(location=[dos_rainfall['latitude'].mean(), dos_rainfall['longitude'].mean()], zoom_start=10)

        for idx, row in dos_rainfall.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=row['rainfall']/50, color='blue', fill_color='blue').add_to(m)

        for idx, row in kurty_flow.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=row['flow']/100, color='red', fill_color='red').add_to(m)

        m.save("133.html")