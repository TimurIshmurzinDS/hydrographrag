python
       import pandas as pd

       # Замените 'data_source.csv' на фактический путь к источнику данных
       data = pd.read_csv('data_source.csv')

       # Фильтрация данных для реки Батарейка
       batareyka_river_data = data[data['River'] == 'Batareyka River']

       # Получение текущего уровня воды в реке Батарейка
       current_water_level = batareyka_river_data['Water_level_Value'].iloc[-1]

       print(f"Текущий уровень воды в реке Батарейка: {current_water_level}")