python
        import pandas as pd
        import geopandas as gpd
        import folium

        # Загрузка данных
        data_2015 = pd.read_csv('water_levels_2015.csv')
        data_2023 = pd.read_csv('water_levels_2023.csv')

        # Преобразование в GeoDataFrame
        gdf_2015 = gpd.GeoDataFrame(data_2015, geometry=gpd.points_from_xy(data_2015.longitude, data_2015.latitude))
        gdf_2023 = gpd.GeoDataFrame(data_2023, geometry=gpd.points_from_xy(data_2023.longitude, data_2023.latitude))

        # Создание столбца с разницей уровней воды
        gdf_2015['diff'] = gdf_2023['water_level'] - gdf_2015['water_level']

        # Создание карты
        m = folium.Map(location=[gdf_2015.geometry.y.mean(), gdf_2015.geometry.x.mean()], zoom_start=10)

        # Добавление данных на карту
        for idx, row in gdf_2015.iterrows():
            folium.CircleMarker(location=[row.geometry.y, row.geometry.x],
                                radius=6,
                                color='red' if row['diff'] > 0 else 'blue',
                                fill_color='red' if row['diff'] > 0 else 'blue').add_to(m)

        # Сохранение карты
        m.save("49.html")