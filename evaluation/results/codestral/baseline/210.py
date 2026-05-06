python
        import pandas as pd
        from scipy import stats
        import matplotlib.pyplot as plt
        import folium

        # Загрузка данных
        lepsy_data = pd.read_csv('lepsy_river_data.csv')
        aksu_data = pd.read_csv('aksu_river_data.csv')

        # Предобработка данных
        lepsy_data['date'] = pd.to_datetime(lepsy_data['date'])
        aksu_data['date'] = pd.to_datetime(aksu_data['date'])

        # Разделение по сезонам
        seasons = [('winter', (1, 2, 12)), ('spring', (3, 4, 5)), ('summer', (6, 7, 8)), ('autumn', (9, 10, 11))]
        lepsy_data['season'] = lepsy_data['date'].dt.month.apply(lambda x: [s for s, m in seasons if x in m][0])
        aksu_data['season'] = aksu_data['date'].dt.month.apply(lambda x: [s for s, m in seasons if x in m][0])

        # Вычисление средних значений стока для каждого сезона
        lepsy_seasonal_flow = lepsy_data.groupby('season')['flow'].mean()
        aksu_seasonal_flow = aksu_data.groupby('season')['flow'].mean()

        # Статистический анализ
        t_stat, p_value = stats.ttest_ind(lepsy_data['flow'], aksu_data['flow'])
        print(f'T-статистика: {t_stat}, P-значение: {p_value}')

        # Визуализация на карте с использованием folium
        m = folium.Map(location=[42, 69], zoom_start=5)
        folium.Choropleth(geo_data='world-countries.json', data=lepsy_seasonal_flow, key_on='feature.id').add_to(m)
        m.save("210.html")

        # Графическое представление сравнения
        plt.figure(figsize=(10, 6))
        lepsy_seasonal_flow.plot(kind='bar', color='blue', alpha=0.7, label='Lepsy River')
        aksu_seasonal_flow.plot(kind='bar', color='red', alpha=0.7, label='Aksu River')
        plt.title('Seasonal Flow Comparison')
        plt.xlabel('Season')
        plt.ylabel('Flow')
        plt.legend()
        plt.show()