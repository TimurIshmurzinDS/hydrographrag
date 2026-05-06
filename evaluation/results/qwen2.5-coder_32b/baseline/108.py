import pandas as pd
import numpy as np
from scipy import stats
import folium

# Предположим, что у нас есть данные в формате CSV с колонками: 'date', 'river', 'discharge'
# Пример данных:
data = {
    'date': pd.date_range(start='2023-01-01', periods=365*2, freq='D').tolist() * 2,
    'river': ['Kurty River'] * 730 + ['Urzhar River'] * 730,
    'discharge': np.random.normal(loc=100, scale=20, size=1460) + np.sin(np.linspace(0, 2*np.pi, 1460)) * 50
}
df = pd.DataFrame(data)

# Преобразование даты в формат datetime
df['date'] = pd.to_datetime(df['date'])

# Группировка данных по рекам и дате для вычисления среднего уровня стока за каждый день
daily_discharge = df.groupby(['river', 'date']).mean().reset_index()

# Вычисление разницы между текущим уровнем стока и средним значением за предыдущий год
daily_discharge['yearly_avg'] = daily_discharge.groupby('river')['discharge'].transform(lambda x: x.rolling(window=365, min_periods=1).mean())
daily_discharge['discharge_diff'] = daily_discharge['discharge'] - daily_discharge['yearly_avg']

# Определение признаков экологического стресса (например, значительное отклонение от среднего)
daily_discharge['stress_flag'] = np.abs(daily_discharge['discharge_diff']) > 2 * daily_discharge.groupby('river')['discharge_diff'].transform(lambda x: x.std())

# Фильтрация данных для участков с признаками экологического стресса
stress_points = daily_discharge[daily_discharge['stress_flag']]

# Предположим, что у нас есть координаты рек (примерные данные)
river_coords = {
    'Kurty River': [51.2345, 76.8901],
    'Urzhar River': [51.5678, 77.2345]
}

# Создание карты с помощью folium
m = folium.Map(location=[51.4014, 77.0475], zoom_start=9)

# Добавление маркеров на карту для участков с признаками экологического стресса
for index, row in stress_points.iterrows():
    river_name = row['river']
    if river_name in river_coords:
        folium.Marker(
            location=river_coords[river_name],
            popup=f"{river_name} - Признаки экологического стресса: {row['date']}",
            icon=folium.Icon(color='red')
        ).add_to(m)

# Сохранение карты в файл
m.save("108.html")