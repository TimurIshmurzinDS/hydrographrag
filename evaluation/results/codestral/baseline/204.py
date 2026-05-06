python
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        import folium

        # Шаг 1: Загрузка данных
        byzhy_data = pd.read_csv('byzhy_river_discharge.csv')
        urzhar_data = pd.read_csv('urzhar_river_discharge.csv')

        # Шаг 2: Предварительный анализ данных
        print(byzhy_data.describe())
        print(urzhar_data.describe())

        # Шаг 3: Статистический анализ
        byzhy_stats = byzhy_data['discharge'].describe()
        urzhar_stats = urzhar_data['discharge'].describe()
        print("Byzhy River Stats:\n", byzhy_stats)
        print("\nUrzhar River Stats:\n", urzhar_stats)

        # Шаг 4: Визуализация данных
        plt.figure(figsize=(10,5))
        sns.lineplot(data=byzhy_data, x='date', y='discharge', label='Byzhy River')
        sns.lineplot(data=urzhar_data, x='date', y='discharge', label='Urzhar River')
        plt.title('Discharge Comparison Between Byzhy and Urzhar Rivers')
        plt.legend()
        plt.show()

        # Шаг 5: Создание карты (пример кода, замените координаты на реальные)
        m = folium.Map(location=[55.751244, 37.618423], zoom_start=10)
        folium.Marker([55.751244, 37.618423], popup='Byzhy River').add_to(m)
        folium.Marker([55.761244, 37.628423], popup='Urzhar River').add_to(m)
        m.save("204.html")