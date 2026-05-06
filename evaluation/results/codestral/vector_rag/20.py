python
       import pandas as pd

       # Загрузка данных
       data = pd.read_csv('data/river_data.csv')  # Предполагается, что данные сохранены в формате CSV

       # Преобразование даты в формат datetime
       data['Date_water_level_Value'] = pd.to_datetime(data['Date_water_level_Value'])

       # Определение периода паводка (пример: с 1 января по 31 марта)
       flood_period = data[(data['Date_water_level_Value'].dt.month >= 1) & (data['Date_water_level_Value'].dt.month <= 3)]

       # Анализ изменений расхода воды в период паводка
       flood_period_consumption = flood_period['Water_consumption_Value']
       print(flood_period_consumption.describe())