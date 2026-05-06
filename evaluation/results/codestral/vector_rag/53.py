python
   import pandas as pd

   # Загрузка данных (предполагается, что данные доступны в виде CSV-файлов)
   data_2021 = pd.read_csv('data/water_quality_2021.csv')
   data_2022 = pd.read_csv('data/water_quality_2022.csv')

   # Извлечение значений температуры воды для каждого года
   temp_2021 = data_2021['HM_Water_quality_class_2021_2022Parameter'].where(data_2021['HM_Water_quality_class_2021_2022Unit'] == '°C')
   temp_2022 = data_2022['HM_Water_quality_class_2020_2021Parameter'].where(data_2022['HM_Water_quality_class_2020_2021Unit'] == '°C')

   # Статистический анализ данных для каждого года
   mean_temp_2021 = temp_2021.mean()
   mean_temp_2022 = temp_2022.mean()

   # Сравнение показателей и интерпретация результатов
   if mean_temp_2021 > mean_temp_2022:
       print("Средняя температура воды в реке Шилик в 2021 году была выше, чем в 2022 году.")
   elif mean_temp_2021 < mean_temp_2022:
       print("Средняя температура воды в реке Шилик в 2021 году была ниже, чем в 2022 году.")
   else:
       print("Средняя температура воды в реке Шилик в 2021 и 2022 годах была одинакова.")