import pandas as pd
from folium import Map, Marker
import numpy as np

# Сбор данных (предположим, что данные хранятся в DataFrame)
data = {
    'year': [2020, 2021, 2022],
    'water_level': [10.5, 12.8, 9.2],
    'pasta_prepared': [True, False, True]
}
df = pd.DataFrame(data)

# Анализ данных
correlation = df['water_level'].corr(df['pasta_prepared'])
print(f'Корреляция между уровнем воды и приготовлением пасты: {correlation}')

# Создание гео-модели (предположим, что мы используем линейную регрессию)
from sklearn.linear_model import LinearRegression
X = df[['water_level']]
y = df['pasta_prepared']
model = LinearRegression()
model.fit(X, y)

# Визуализация результатов на карте
m = Map(location=[43.1234, 77.4567], zoom_start=10)
for i in range(len(df)):
    marker = Marker(location=[df.iloc[i]['year'], df.iloc[i]['water_level']], popup=f'Год: {df.iloc[i]["year"]}, Уровень воды: {df.iloc[i]["water_level"]}').add_to(m)
m.save("231.html")