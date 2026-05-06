python
        # Импортируем необходимые библиотеки
        import geopandas as gpd
        import folium

        # Загружаем данные о реках Шарын и Уржар
        sharin = gpd.read_file('sharin_data.geojson')
        urjar = gpd.read_file('urjar_data.geojson')

        # Сравниваем экологический статус речных экосистем в бассейнах
        comparison = sharin.merge(urjar, on='basin', suffixes=('_sharin', '_urjar'))

        # Создаем карту с помощью folium
        m = folium.Map(location=[comparison['lat'].mean(), comparison['lon'].mean()], zoom_start=6)

        # Добавляем данные о бассейнах рек Шарын на карту
        for _, r in comparison.iterrows():
            folium.GeoJson(r['geometry_sharin'], style_function=lambda x, color='green' if r['ecological_status_sharin'] == 'good' else 'red').add_to(m)

        # Добавляем данные о бассейнах рек Уржар на карту
        for _, r in comparison.iterrows():
            folium.GeoJson(r['geometry_urjar'], style_function=lambda x, color='green' if r['ecological_status_urjar'] == 'good' else 'red').add_to(m)

        # Сохраняем карту в файл
        m.save("188.html")