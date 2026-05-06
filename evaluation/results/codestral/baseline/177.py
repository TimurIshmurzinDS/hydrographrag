python
        import geopandas as gpd
        import pandas as pd
        from shapely.geometry import shape
        import pygeos
        import folium

        # Шаг 2: Загрузка данных
        sarykan_basin = gpd.read_file('sarykan_basin.geojson')
        emel_basin = gpd.read_file('emel_basin.geojson')

        # Шаг 3: Создание нового столбца для топологической сложности
        sarykan_basin['topological_complexity'] = None
        emel_basin['topological_complexity'] = None

        # Шаг 4: Вычисление топологической сложности
        for i in range(len(sarykan_basin)):
            sarykan_basin.loc[i, 'topological_complexity'] = pygeos.topological_complexity(shape(sarykan_basin.geometry[i]))

        for i in range(len(emel_basin)):
            emel_basin.loc[i, 'topological_complexity'] = pygeos.topological_complexity(shape(emel_basin.geometry[i]))

        # Шаг 5: Объединение данных
        basins = pd.concat([sarykan_basin, emel_basin])

        # Шаг 6: Визуализация на карте с помощью folium
        m = folium.Map(location=[basins['geometry'].centroid.y.mean(), basins['geometry'].centroid.x.mean()], zoom_start=10)

        for _, r in basins.iterrows():
            sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance=0.001)
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j, style_function=lambda x: {'fillColor': 'green' if r['river'] == 'Sarykan' else 'blue',
                                                                         'color': 'black',
                                                                         'weight': 2,
                                                                         'opacity': 1,
                                                                         'fillOpacity': 0.6})
            folium.Popup(f"River: {r['river']}<br>Topological Complexity: {r['topological_complexity']}").add_to(geo_j)
            geo_j.add_to(m)

        # Шаг 7: Сохранение карты в файл
        m.save("177.html")