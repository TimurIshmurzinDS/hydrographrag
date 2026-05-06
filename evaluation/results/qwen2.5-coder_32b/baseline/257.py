import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с историческими данными о уровне воды в реке Баянколь
data = pd.read_csv('bayan_kol_water_level.csv', parse_dates=['date'], index_col='date')

# Допустим, у нас также есть данные о потребности в воде для полива (в кубометрах)
irrigation_needs = pd.read_csv('irrigation_needs.csv', parse_dates=['date'], index_col='date')

# Шаг 2: Обработка данных
# Удаление пропусков и аномалий
data.dropna(inplace=True)

# Нормализация данных (если необходимо)
data['water_level'] = (data['water_level'] - data['water_level'].mean()) / data['water_level'].std()

# Шаг 3: Моделирование
# Используем простую линейную регрессию для предсказания уровня воды на основе даты
X = np.array(data.index.map(pd.Timestamp.toordinal)).reshape(-1, 1)
y = data['water_level'].values

model = LinearRegression()
model.fit(X, y)

# Предсказание уровня воды на текущую дату
current_date = pd.Timestamp.now().toordinal()
predicted_water_level = model.predict(np.array([[current_date]]))[0]

# Шаг 4: Расчет потребности в поливе
# Предположим, что потребность в воде зависит от уровня воды в реке
# Например, если уровень воды ниже среднего, то потребность в поливе увеличивается

average_water_level = data['water_level'].mean()
if predicted_water_level < average_water_level:
    irrigation_need_today = irrigation_needs.loc[pd.Timestamp.now().date(), 'need'] * 1.2
else:
    irrigation_need_today = irrigation_needs.loc[pd.Timestamp.now().date(), 'need']

# Шаг 5: Визуализация
# Создание карты с использованием folium
m = folium.Map(location=[43.069, 78.21], zoom_start=10)  # Координаты Баян-Кола

# Добавление маркера с информацией о потребности в воде для полива
folium.Marker(
    location=[43.069, 78.21],
    popup=f"Потребность в воде для полива: {irrigation_need_today} кубометров",
    icon=folium.Icon(color='blue')
).add_to(m)

# Сохранение карты
m.save("257.html")

print(f"Предсказанный уровень воды: {predicted_water_level}")
print(f"Текущая потребность в воде для полива: {irrigation_need_today} кубометров")