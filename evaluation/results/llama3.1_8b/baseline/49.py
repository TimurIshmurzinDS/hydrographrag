import pandas as pd
from folium import Map, Marker

# Загрузка данных о уровнях воды для 2015 года
data_2015 = pd.read_csv('batareyka_2015.csv')

# Загрузка данных о уровнях воды для 2023 года
data_2023 = pd.read_csv('batareyka_2023.csv')

# Обработка данных, чтобы получить пиковые значения для каждого года
max_values_2015 = data_2015.loc[data_2015['water_level'].idxmax()]
max_values_2023 = data_2023.loc[data_2023['water_level'].idxmax()]

# Сравнение пиковых значений между двумя годами
if max_values_2015['water_level'] > max_values_2023['water_level']:
    print('Пиковый уровень воды в 2015 году был выше, чем в 2023 году.')
elif max_values_2015['water_level'] < max_values_2023['water_level']:
    print('Пиковый уровень воды в 2023 году был выше, чем в 2015 году.')
else:
    print('Пиковые уровни воды в 2015 и 2023 годах были одинаковыми.')

# Визуализация результатов на карте
m = Map(location=[55.75, 37.62], zoom_start=12)
Marker(location=[55.75, 37.62], popup='Пиковый уровень воды в 2015 году').add_to(m)
Marker(location=[55.75, 37.62], popup='Пиковый уровень воды в 2023 году').add_to(m)

# Сохранение карты
m.save('batareyka.html')