import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import folium

# Пример данных (замените на реальные данные)
data = {
    'Year': [2018, 2019, 2020, 2021, 2022],
    'WaterConsumption': [100, 150, 120, 130, 140],  # объем потребления воды из реки Бызж
    'Yield': [2000, 2200, 2100, 2300, 2400]  # урожайность местных культур
}

# Создание DataFrame
df = pd.DataFrame(data)

# Препроцессинг данных (проверка на пропущенные значения)
if df.isnull().any().any():
    print("В данных есть пропущенные значения.")
else:
    print("Данные очищены от пропущенных значений.")

# Анализ корреляции
correlation, p_value = pearsonr(df['WaterConsumption'], df['Yield'])
print(f"Корреляция между объемом потребления воды и урожайностью: {correlation}")
print(f"P-value: {p_value}")

# Визуализация данных на карте
m = folium.Map(location=[50.45, 30.52], zoom_start=10)

for index, row in df.iterrows():
    folium.Marker(
        location=[50.45 + np.random.uniform(-0.1, 0.1), 30.52 + np.random.uniform(-0.1, 0.1)],
        popup=f"Год: {row['Year']}, Вода: {row['WaterConsumption']}, Урожай: {row['Yield']}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

m.save("185.html")