python
        import pandas as pd
        import folium

        # Шаг 1: Загрузка данных
        data = pd.read_csv('kurty_river_data.csv')

        # Предполагается, что в данных есть столбцы 'season' (лето или зима) и 'water_flow' (расход воды)

        # Шаг 2: Разделение данных на летний и зимний периоды
        summer_data = data[data['season'] == 'summer']
        winter_data = data[data['season'] == 'winter']

        # Шаг 3: Вычисление среднего расхода воды для каждого периода
        avg_summer_flow = summer_data['water_flow'].mean()
        avg_winter_flow = winter_data['water_flow'].mean()

        # Шаг 4: Сравнение средних значений
        if avg_summer_flow > avg_winter_flow:
            print("Средний расход воды в реке Kurty River в летний период выше, чем в зимний.")
        elif avg_summer_flow < avg_winter_flow:
            print("Средний расход воды в реке Kurty River в зимний период выше, чем в летний.")
        else:
            print("Средний расход воды в реке Kurty River одинаков в летний и зимний периоды.")

        # Шаг 5: Визуализация на карте (пример с использованием библиотеки folium)
        m = folium.Map(location=[55, 60], zoom_start=10)

        # Добавление маркеров для среднего расхода воды в летний и зимний периоды
        folium.Marker([55, 60], popup=f"Средний расход воды в летний период: {avg_summer_flow}").add_to(m)
        folium.Marker([54, 60], popup=f"Средний расход воды в зимний период: {avg_winter_flow}").add_to(m)

        # Сохранение карты
        m.save("51.html")