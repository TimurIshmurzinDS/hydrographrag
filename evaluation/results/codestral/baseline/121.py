python
        # Импортируем необходимые библиотеки
        import pandas as pd
        import folium

        # Загружаем данные
        bayankol_data = pd.read_csv('bayankol_river_data.csv')
        shilik_data = pd.read_csv('shilik_river_data.csv')

        # Проверяем данные на пропуски и аномалии (этот шаг может быть более сложным в зависимости от конкретных данных)
        bayankol_data = bayankol_data.dropna()
        shilik_data = shilik_data.dropna()

        # Вычисляем средний расход воды для каждой реки за каждый год
        bayankol_avg = bayankol_data.groupby('year')['water_flow'].mean()
        shilik_avg = shilik_data.groupby('year')['water_flow'].mean()

        # Создаем карту
        m = folium.Map(location=[55, 100], zoom_start=4)

        # Добавляем данные на карту (здесь предполагается, что у вас есть координаты рек)
        for year in bayankol_avg.index:
            folium.Marker(location=[bayankol_river_lat, bayankol_river_lon], popup=f'Bayankol River - Year: {year}, Avg Water Flow: {bayankol_avg[year]}').add_to(m)
            folium.Marker(location=[shilik_river_lat, shilik_river_lon], popup=f'Shilik River - Year: {year}, Avg Water Flow: {shilik_avg[year]}').add_to(m)

        # Сохраняем карту
        m.save("121.html")