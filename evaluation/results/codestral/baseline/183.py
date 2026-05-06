python
        import geopandas as gpd
        import rasterio
        from rasterstats import zonal_stats
        import folium

        # 1. Получение данных о состоянии реки Турген (предполагается наличие растрового файла)
        river_data = rasterio.open('river_turghen_data.tif')

        # 2. Создание геопространственной модели доступности воды для орошения садов
        def calculate_water_availability(garden_data, river_stats):
            garden_data['water_availability'] = (garden_data['water_demand'] / river_stats[0]['mean']) * 100
            return garden_data

        # 3. Оценка доступности воды для садов
        gardens = gpd.read_file('gardens.shp')
        gardens['water_demand'] = 50  # Предполагается, что потребность в воде указана для каждого сада
        river_stats = zonal_stats(gardens, 'river_turghen_data.tif', stats='mean')
        gardens = calculate_water_availability(gardens, river_stats)

        # 4. Визуализация результатов на карте с использованием библиотеки folium
        m = folium.Map(location=[55.76, 37.61], zoom_start=10)
        chloropleth = folium.Choropleth(
            geo_data=gardens,
            data=gardens,
            columns=['GID', 'water_availability'],
            key_on='feature.properties.GID',
            fill_color='YlGnBu',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Water Availability for Irrigation (%)'
        )
        chloropleth.geojson.add_to(m)
        m.save("183.html")