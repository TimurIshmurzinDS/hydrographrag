python
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import folium

        # Шаг 1: Загрузка данных
        temirlik_data = pd.read_csv('temirlik_river_data.csv')
        turgen_data = pd.read_csv('turgen_river_data.csv')

        # Шаг 2: Предобработка данных
        temirlik_data = temirlik_data.dropna()
        turgen_data = turgen_data.dropna()

        # Шаг 3: Анализ сезонных динамик расхода воды
        temirlik_seasonal = temirlik_data.groupby(temirlik_data['date'].dt.month)['water_flow'].mean()
        turgen_seasonal = turgen_data.groupby(turgen_data['date'].dt.month)['water_flow'].mean()

        # Шаг 4: Сравнение результатов
        plt.figure(figsize=(10,6))
        sns.lineplot(x=temirlik_seasonal.index, y=temirlik_seasonal.values, label='Temirlik River')
        sns.lineplot(x=turgen_seasonal.index, y=turgen_seasonal.values, label='Turgen River')
        plt.title('Seasonal Dynamics of Water Flow')
        plt.legend()
        plt.show()

        # Шаг 5: Визуализация на карте
        m = folium.Map(location=[42, 69], zoom_start=7)
        folium.PolyLine(locations=temirlik_data[['latitude', 'longitude']].values, color='blue').add_to(m)
        folium.PolyLine(locations=turgen_data[['latitude', 'longitude']].values, color='red').add_to(m)
        m.save("83.html")