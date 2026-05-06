python
        import folium
        import geopandas as gpd

        # Загрузка данных о гидрологических постах
        hydro_posts = gpd.read_file('hydro_posts.geojson')

        # Определение критического уровня (пример: 5 метров)
        critical_level = 5

        # Фильтрация данных для отображения только постов с критическим уровнем
        critical_posts = hydro_posts[hydro_posts['water_level'] > critical_level]

        # Создание карты
        m = folium.Map(location=[critical_posts['lat'].mean(), critical_posts['lon'].mean()], zoom_start=10)

        # Добавление маркеров на карту для каждого гидрологического поста с критическим уровнем
        for idx, row in critical_posts.iterrows():
            folium.Marker([row['lat'], row['lon']], popup=f'Water Level: {row["water_level"]}').add_to(m)

        # Сохранение карты
        m.save("70.html")