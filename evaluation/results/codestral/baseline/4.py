python
        import folium
        import geopandas as gpd

        # Загрузка данных о станциях мониторинга на реке Koktal River
        stations = gpd.read_file('koktal_river_stations.geojson')

        # Создание карты с центром в средней точке всех станций
        m = folium.Map(location=[stations['geometry'].y.mean(), stations['geometry'].x.mean()], zoom_start=10)

        # Добавление маркеров на карту для каждой станции мониторинга
        for idx, row in stations.iterrows():
            if row['status'] == 'working':
                color = 'green'
            else:
                color = 'red'
            folium.Marker([row['geometry'].y, row['geometry'].x], icon=folium.Icon(color=color)).add_to(m)

        # Сохранение карты как HTML-файл
        m.save("4.html")