python
        import pandas as pd
        import geopandas as gpd
        from shapely.geometry import Point
        import folium
        from sklearn.ensemble import RandomForestRegressor

        # Шаг 1: Загрузка данных
        river_data = gpd.read_file('river_urjar.shp')
        irrigation_data = pd.read_csv('irrigation_systems.csv')
        water_quality_data = pd.read_csv('water_quality.csv')

        # Шаг 2: Определение зон риска
        buffer_distance = 500  # метры
        risk_zones = river_data.buffer(buffer_distance)

        # Шаг 3: Создание модели
        irrigation_data['distance_to_river'] = irrigation_data.apply(lambda row: river_data.distance(Point(row['longitude'], row['latitude'])).min(), axis=1)
        data = pd.merge(irrigation_data, water_quality_data, on='location_id')
        X = data[['distance_to_river', 'water_salinity', 'irrigation_efficiency']]
        y = data['soil_salinization']
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)

        # Шаг 4: Визуализация результатов
        data['predicted_salinization'] = model.predict(X)
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
        for _, row in data.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], radius=5, color='red', fill=True, fill_color='red', fill_opacity=row['predicted_salinization']/10).add_to(m)
        m.save("195.html")