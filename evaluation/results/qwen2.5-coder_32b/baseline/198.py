import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium

# Предполагаемые данные для уровня воды (замените на реальные данные)
data = {
    'date': pd.date_range(start='1980-01-01', periods=4380, freq='M'),  # 365 месяцев * 12 лет
    'lepsy_water_level': np.random.normal(loc=150, scale=10, size=4380),
    'turgeon_water_level': np.random.normal(loc=170, scale=15, size=4380)
}

df = pd.DataFrame(data)

# Преобразование даты в числовой формат для модели линейной регрессии
df['date_numeric'] = (df['date'] - df['date'].min()).dt.days

# Модель линейной регрессии для уровня воды реки Lepsy
X_lepsy = df[['date_numeric']]
y_lepsy = df['lepsy_water_level']
model_lepsy = LinearRegression().fit(X_lepsy, y_lepsy)
df['trend_lepsy'] = model_lepsy.predict(X_lepsy)

# Модель линейной регрессии для уровня воды реки Turgen
X_turgeon = df[['date_numeric']]
y_turgeon = df['turgeon_water_level']
model_turgeon = LinearRegression().fit(X_turgeon, y_turgeon)
df['trend_turgeon'] = model_turgeon.predict(X_turgeon)

# Визуализация данных и трендов
plt.figure(figsize=(14, 7))
plt.plot(df['date'], df['lepsy_water_level'], label='Уровень воды Lepsy River', alpha=0.5)
plt.plot(df['date'], df['trend_lepsy'], label='Тренд Lepsy River', color='red')
plt.plot(df['date'], df['turgeon_water_level'], label='Уровень воды Turgen River', alpha=0.5)
plt.plot(df['date'], df['trend_turgeon'], label='Тренд Turgen River', color='blue')
plt.xlabel('Дата')
plt.ylabel('Уровень воды (м)')
plt.title('Долгосрочные тренды изменения уровня воды в реках Lepsy и Turgen')
plt.legend()
plt.grid(True)
plt.show()

# Создание интерактивной карты с помощью folium
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерного центра бассейнов рек

# Добавление маркеров для местоположений рек (замените на реальные координаты)
folium.Marker([42.8673, 74.5910], popup='Lepsy River').add_to(m)
folium.Marker([42.8819, 74.5801], popup='Turgen River').add_to(m)

# Сохранение карты в HTML файл
m.save("198.html")