import pandas as pd
import numpy as np

# Создадим два временных ряда
data1 = {
    'Дата': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Значение 1': [10, 20, 30]
}
df1 = pd.DataFrame(data1)

data2 = {
    'Дата': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'Значение 2': [40, 50, 60]
}
df2 = pd.DataFrame(data2)

# Объединим данные
merged_df = pd.merge(df1, df2, on='Дата')

# Сравним значения
merged_df['Разница'] = merged_df['Значение 1'] - merged_df['Значение 2']

# Визуализируем результат на карте (не требуется в этом случае)
# import folium

# Создадим карту
m = folium.Map(location=[55.7558, 37.6173], zoom_start=10)

# Добавим слой с данными
folium.Marker([55.7558, 37.6173], popup='Разница: ' + str(merged_df['Разница'].iloc[0])).add_to(m)

# Сохраняем карту
m.save("283.html")

print(merged_df)