import pandas as pd
from folium import Map, Marker
import geopandas as gpd

# Сбор данных
data = {
    'water_consumption': [100, 200, 300],
    'temperature_water': [10, 15, 20],
    'level_water': [5, 7, 9],
    'type_plants': ['лес', 'луг', 'озеро'],
    'type_animals': ['рыба', 'птица', 'млекопитающее']
}

df = pd.DataFrame(data)

# Анализ данных
correlation_matrix = df.corr()
print(correlation_matrix)

# Моделирование
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

X = df[['water_consumption', 'temperature_water', 'level_water']]
y = df['type_plants']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor()
model.fit(X_train, y_train)

# Визуализация результатов
m = Map(location=[45.5, 50], zoom_start=10)
for i in range(len(df)):
    marker = Marker(location=[df['temperature_water'].iloc[i], df['level_water'].iloc[i]], popup=df['type_plants'].iloc[i])
    m.add_child(marker)

# Сохранение карты
m.save("36.html")