import pandas as pd
from folium import Map, Marker
import numpy as np

# Данные о расходе воды реки Или (предположим, что они представлены в виде DataFrame)
data = {
    'date': ['2022-01-01', '2022-01-02', '2022-01-03'],
    'water_flow': [1000, 1200, 1100]
}
df = pd.DataFrame(data)

# Создание модели (предположим, что она представляет собой простую линейную зависимость)
def model(water_flow):
    return water_flow * 0.01

# Ввод данных в модель и получение прогноза
predictions = df['water_flow'].apply(model)

# Создание карты с маркерами для каждого дня
m = Map(location=[49.0000, 86.1667], zoom_start=10)
for i in range(len(df)):
    marker = Marker(location=[df.iloc[i]['date'], model(df.iloc[i]['water_flow'])],
                    popup=f'Дата: {df.iloc[i]["date"]}<br>Расход воды: {model(df.iloc[i]["water_flow"])}')
    m.add_child(marker)

# Сохранение карты в файл
m.save("235.html")