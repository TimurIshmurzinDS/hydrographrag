python
        import folium
        import geopandas as gpd
        import requests

        # Загрузка геоданных о реках
        rivers = gpd.read_file('rivers.geojson')

        # Получение данных об уровне воды (замените на фактические данные или API)
        water_levels = {
            'Karaoy River': 5.2,   # Пример уровня воды в метрах
            'Temirlik River': 4.8,
            'Turgen River': 6.1
        }

        # Пороговое значение для опасного роста уровня воды (в метрах)
        threshold = 5.0

        # Определение рек с опасным ростом уровня воды
        at_risk = [river for river, level in water_levels.items() if level > threshold]

        # Создание карты
        m = folium.Map(location=[42.358470, 69.599190], zoom_start=10)

        # Добавление рек на карту
        for idx, row in rivers.iterrows():
            if row['name'] in at_risk:
                color = 'red'
            else:
                color = 'blue'
            folium.GeoJson(row['geometry'], style_function=lambda x, color=color: {'color': color}).add_to(m)

        # Сохранение карты
        m.save("86.html")