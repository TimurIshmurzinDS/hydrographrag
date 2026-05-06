python
        import geopandas as gpd
        import folium

        # Загрузка данных
        karatal_data = gpd.read_file('karatal_hydroposts.geojson')
        lepsa_data = gpd.read_file('lepsa_hydroposts.geojson')

        # Проверка данных
        print(karatal_data.isnull().sum())
        print(lepsa_data.isnull().sum())

        # Определение критериев работоспособности и создание индексов
        karatal_data['operational_index'] = (karatal_data['water_level'] / karatal_data['max_water_level']) * 0.5 + \
                                            (karatal_data['equipment_condition'] / 10) * 0.5
        lepsa_data['operational_index'] = (lepsa_data['water_level'] / lepsa_data['max_water_level']) * 0.5 + \
                                            (lepsa_data['equipment_condition'] / 10) * 0.5

        # Сравнение индексов работоспособности
        comparison_result = karatal_data[['hydropost_id', 'operational_index']].merge(lepsa_data[['hydropost_id', 'operational_index']], on='hydropost_id', suffixes=('_karatal', '_lepsa'))
        comparison_result['difference'] = comparison_result['operational_index_karatal'] - comparison_result['operational_index_lepsa']

        # Визуализация результатов на карте
        m = folium.Map(location=[55, 70], zoom_start=6)

        for idx, row in karatal_data.iterrows():
            folium.CircleMarker([row['geometry'].y, row['geometry'].x], radius=10, color='blue', fill_color='blue').add_to(m)

        for idx, row in lepsa_data.iterrows():
            folium.CircleMarker([row['geometry'].y, row['geometry'].x], radius=10, color='red', fill_color='red').add_to(m)

        m.save("143.html")