python
       import pandas as pd

       # Замените 'historical_data.csv' на фактическое имя вашего файла с историческими данными
       historical_data = pd.read_csv('historical_data.csv')

       # Предположим, что текущие данные о расходе воды хранятся в переменных current_water_consumption и current_water_consumption_m3s
       current_water_consumption = Water_consumption_Value  # Замените на фактическое значение
       current_water_consumption_m3s = Water_consumption_Valuem³s  # Замените на фактическое значение

       # Сравнение текущего расхода воды с историческими данными весеннего паводка
       spring_flood_data = historical_data[historical_data['Season'] == 'Spring Flood']

       if current_water_consumption > spring_flood_data['Water_consumption_Value'].max():
           print("Текущий расход воды на реке Проходная River выше, чем исторические данные весеннего паводка.")
       elif current_water_consumption < spring_flood_data['Water_consumption_Value'].min():
           print("Текущий расход воды на реке Проходная River ниже, чем исторические данные весеннего паводка.")
       else:
           print("Текущий расход воды на реке Проходная River находится в пределах исторических данных весеннего паводка.")

       # Аналогично можно сравнить current_water_consumption_m3s с spring_flood_data['Water_consumption_Valuem³s']