python
         import geopandas as gpd
         import folium
         from branca.colormap import LinearColormap
         # Загрузка данных
         data_19th = gpd.read_file('gold_mining_19th_century.geojson')
         data_20th = gpd.read_file('gold_mining_20th_century.geojson')
         # Обработка данных
         data_19th = data_19th.dropna()
         data_20th = data_20th.dropna()
         # Создание карты
         m = folium.Map(location=[55, 100], zoom_start=4)
         # Цветовая шкала
         colormap_19th = LinearColormap(['yellow', 'red'], vmin=data_19th['gold'].min(), vmax=data_19th['gold'].max())
         colormap_20th = LinearColormap(['blue', 'green'], vmin=data_20th['gold'].min(), vmax=data_20th['gold'].max())
         # Добавление слоев на карту
         folium.GeoJson(
             data_19th,
             style_function=lambda x: {
                 'fillColor': colormap_19th(x['properties']['gold']),
                 'color': 'black',
                 'weight': 2,
                 'dashArray': '5, 5'
             },
             tooltip=folium.GeoJsonTooltip(fields=['name', 'gold'], aliases=['Место добычи: ', 'Количество золота: '], labels=True)
         ).add_to(m)
         folium.GeoJson(
             data_20th,
             style_function=lambda x: {
                 'fillColor': colormap_20th(x['properties']['gold']),
                 'color': 'black',
                 'weight': 2,
                 'dashArray': '5, 5'
             },
             tooltip=folium.GeoJsonTooltip(fields=['name', 'gold'], aliases=['Место добычи: ', 'Количество золота: '], labels=True)
         ).add_to(m)
         # Добавление легенды
         colormap_19th.caption = 'Добыча золота в XIX веке'
         colormap_20th.caption = 'Добыча золота в XX веке'
         m.add_child(colormap_19th)
         m.add_child(colormap_20th)
         # Сохранение карты
         m.save("274.html")