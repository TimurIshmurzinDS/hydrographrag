import pandas as pd
from folium import Map, CircleMarker
import matplotlib.pyplot as plt

# Шаг 1: Сбор данных о расходе воды в реках Курты и Текес за последние 5 лет.
data_kurty = {
    'Дата': ['2020-03-01', '2020-04-01', '2021-03-01', '2022-03-01', '2023-03-01'],
    'Расход воды (м³)': [100, 120, 110, 130, 125]
}

data_tekes = {
    'Дата': ['2020-04-01', '2021-04-01', '2022-04-01', '2023-04-01', '2024-04-01'],
    'Расход воды (м³)': [150, 160, 155, 165, 170]
}

df_kurty = pd.DataFrame(data_kurty)
df_tekes = pd.DataFrame(data_tekes)

# Шаг 2: Подготовка данных к анализу.
# Очистка и преобразование формата данных.
df_kurty['Дата'] = pd.to_datetime(df_kurty['Дата'])
df_tekes['Дата'] = pd.to_datetime(df_tekes['Дата'])

# Объединение данных по дате.
merged_data = pd.merge(df_kurty, df_tekes, on='Дата', suffixes=('_kurty', '_tekes'))

# Шаг 3: Анализ данных.
# Определение средних значений расхода воды в обеих реках за период весеннего половодья.
mean_flow_kurty = merged_data['Расход воды (м³)_kurty'].mean()
mean_flow_tekes = merged_data['Расход воды (м³)_tekes'].mean()

print(f'Средний расход воды в реке Курты: {mean_flow_kurty} м³')
print(f'Средний расход воды в реке Текес: {mean_flow_tekes} м³')

# Шаг 4: Визуализация результатов на карте.
m = Map(location=[50.0, 70.0], zoom_start=6)

# Добавление маркеров для показателей расхода воды в обеих реках.
CircleMarker([50.0, 70.0], radius=10).add_to(m)
CircleMarker([55.0, 75.0], radius=15).add_to(m)

# Визуализация средних значений расхода воды на карте.
plt.scatter(merged_data['Расход воды (м³)_kurty'], merged_data['Расход воды (м³)_tekes'])
plt.xlabel('Расход воды в реке Курты')
plt.ylabel('Расход воды в реке Текес')
plt.title('Сравнение показателей расхода воды в реках Курты и Текес')

# Сохранение карты.
m.save("129.html")