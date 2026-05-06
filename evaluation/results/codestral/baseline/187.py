python
        import geopandas as gpd
        from shapely.geometry import Point
        from sklearn.linear_model import LinearRegression
        import folium
        from scipy.spatial.distance import cdist
        import numpy as np

        # Загрузка данных о реке Токыраун и животноводческих хозяйствах
        river = gpd.read_file('river_data.shp')
        farms = gpd.read_file('farms_data.shp')

        # Определение влияния снижения уровня реки на каждое животноводческое хозяйство
        river_buffer = river.geometry.buffer(1000)  # Создание буферной зоны вокруг реки
        farms['river_distance'] = farms.apply(lambda row: min(cdist([row.geometry], [pt for pt in river_buffer[0].exterior.coords])), axis=1)

        # Определение связи между изменением уровня реки и потреблением воды животноводческими хозяйствами
        X = farms['river_distance'].values.reshape(-1, 1)
        Y = farms['water_consumption'].values.reshape(-1, 1)
        regressor = LinearRegression()
        regressor.fit(X, Y)

        # Визуализация результатов на карте
        m = folium.Map(location=[farms['geometry'].y.mean(), farms['geometry'].x.mean()], zoom_start=10)
        for idx, row in farms.iterrows():
            folium.CircleMarker([row['geometry'].y, row['geometry'].x],
                                radius=np.sqrt(row['water_consumption']) * 2,
                                color='red',
                                fill=True,
                                fill_color='red').add_to(m)
        m.save("187.html")