python
        import pandas as pd
        import numpy as np
        import folium
        from scipy.stats import genpareto

        # Загрузка данных
        data = pd.read_csv('koksu_river_data.csv')

        # Определение порога паводка
        threshold = data['water_level'].max()

        # Расчет вероятности превышения порога
        exceedances = data[data['water_level'] > threshold]
        probabilities = [len(exceedances[exceedances.index < year]) / len(data[data.index < year]) for year in data.index]

        # Добавление вероятностей в данные
        data['probability_of_exceedance'] = probabilities

        # Визуализация на карте
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

        for i in range(len(data)):
            folium.CircleMarker(
                location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                radius=5,
                color='red' if data.iloc[i]['water_level'] > threshold else 'blue',
                fill=True,
                fill_color='red' if data.iloc[i]['water_level'] > threshold else 'blue',
                popup=f"Year: {data.index[i]}, Water Level: {data.iloc[i]['water_level']}, Probability of Exceedance: {data.iloc[i]['probability_of_exceedance']}"
            ).add_to(m)

        m.save("203.html")