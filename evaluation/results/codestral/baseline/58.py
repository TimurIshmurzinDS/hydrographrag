python
        import pandas as pd
        import folium

        # Шаг 1: Загрузка данных
        data_2020 = pd.read_csv('sarykan_river_2020.csv')
        data_2023 = pd.read_csv('sarykan_river_2023.csv')

        # Шаг 2: Проверка данных
        print(data_2020.isnull().sum())
        print(data_2023.isnull().sum())

        # Шаг 3: Группировка данных по месяцам
        data_2020['month'] = pd.DatetimeIndex(data_2020['date']).month
        data_2023['month'] = pd.DatetimeIndex(data_2023['date']).month

        monthly_2020 = data_2020.groupby('month')['water_discharge'].mean()
        monthly_2023 = data_2023.groupby('month')['water_discharge'].mean()

        # Шаг 5: Визуализация данных на карте с использованием folium
        m = folium.Map(location=[51.18, 71.45], zoom_start=6)

        folium.Line(
            locations=[monthly_2020.index, monthly_2020.values],
            color='blue',
            popup='2020'
        ).add_to(m)

        folium.Line(
            locations=[monthly_2023.index, monthly_2023.values],
            color='red',
            popup='2023'
        ).add_to(m)

        m.save("58.html")