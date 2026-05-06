python
        import pandas as pd
        import numpy as np
        import folium
        from scipy import stats

        # Шаг 1: Сбор данных
        lepsy_data = pd.read_csv('lepsy_river_data.csv')
        shilik_data = pd.read_csv('shilik_river_data.csv')

        # Шаг 2: Предобработка данных
        lepsy_data = lepsy_data.dropna()
        shilik_data = shilik_data.dropna()

        # Шаг 3: Разделение на сезоны
        seasons = {12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
                   6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
        lepsy_data['Season'] = lepsy_data['Month'].map(seasons)
        shilik_data['Season'] = shilik_data['Month'].map(seasons)

        # Шаг 4: Оценка сезонного стока
        lepsy_seasonal_flow = lepsy_data.groupby('Season')['Flow'].agg([np.mean, np.std])
        shilik_seasonal_flow = shilik_data.groupby('Season')['Flow'].agg([np.mean, np.std])

        # Шаг 5: Визуализация на карте
        m = folium.Map(location=[55, 90], zoom_start=4)

        # Добавление маркеров для Lepsy River
        for season in lepsy_seasonal_flow.index:
            folium.Marker([55, 90], popup=f'Lepsy River - {season}: {lepsy_seasonal_flow["mean"][season]:.2f} ± {lepsy_seasonal_flow["std"][season]:.2f}', icon=folium.Icon(color='blue')).add_to(m)

        # Добавление маркеров для Shilik River
        for season in shilik_seasonal_flow.index:
            folium.Marker([56, 91], popup=f'Shilik River - {season}: {shilik_seasonal_flow["mean"][season]:.2f} ± {shilik_seasonal_flow["std"][season]:.2f}', icon=folium.Icon(color='green')).add_to(m)

        m.save("152.html")