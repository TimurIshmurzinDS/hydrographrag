python
        import geopandas as gpd
        import rasterio
        import folium

        # Загрузка данных
        rivers = gpd.read_file('rivers.shp')
        flora_fauna = gpd.read_file('flora_fauna.shp')

        # Создание буферной зоны вокруг речных побережий
        rivers['geometry'] = rivers.buffer(50)  # Радиус буфера в метрах

        # Определение влияния снижения уровня воды на флору и фауну
        affected_areas = gpd.sjoin(flora_fauna, rivers, how="inner", op='intersects')

        # Оценка экологических последствий (здесь используется простой подсчет)
        impact_score = affected_areas.groupby('id').size()  # id - уникальный идентификатор каждого вида флоры/фауны

        # Визуализация результатов на карте
        m = folium.Map(location=[55, 37], zoom_start=10)

        folium.GeoJson(
            rivers.to_json(),
            style_function=lambda x: {'fillColor': 'blue', 'color': 'blue'}
        ).add_to(m)

        folium.GeoJson(
            affected_areas.to_json(),
            style_function=lambda x: {'fillColor': 'red', 'color': 'red'}
        ).add_to(m)

        m.save("113.html")