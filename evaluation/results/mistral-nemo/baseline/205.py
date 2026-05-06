import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import folium

# 1. Подготовка данных
data_snowmelt = pd.read_csv('snowmelt_data.csv')
data_discharge = pd.read_csv('discharge_data.csv')

# 2. Преобразование данных
X = data_snowmelt['snowmelt_date'].values.reshape(-1, 1)
y = data_discharge['discharge'].values.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Моделирование
model = LinearRegression()
model.fit(X_train, y_train)

# Оценка модели на тестовом наборе данных
accuracy = model.score(X_test, y_test)
print(f'Точность модели: {accuracy}')

# 4. Визуализация
m = folium.Map(location=[56.1300, 92.8333], zoom_start=7) # Координаты реки Лепси

# Добавить данные о сроках снеготаяния и стоке на карту
for i in range(len(data_snowmelt)):
    folium.CircleMarker(location=[data_snowmelt.iloc[i]['latitude'], data_snowmelt.iloc[i]['longitude']],
                        radius=5,
                        color='blue',
                        fill=True).add_to(m)

for i in range(len(data_discharge)):
    folium.CircleMarker(location=[data_discharge.iloc[i]['latitude'], data_discharge.iloc[i]['longitude']],
                        radius=5,
                        color='red',
                        fill=True).add_to(m)

# Сохранить финальную карту
m.save("205.html")