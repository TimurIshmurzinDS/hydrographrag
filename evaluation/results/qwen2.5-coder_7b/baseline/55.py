import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Загрузка исторических данных о уровне воды в реке Batareyka River
data = {
    'Year': [2018, 2019, 2020, 2021, 2022],
    'WaterLevel': [5.2, 5.4, 5.6, 5.8, 6.0]
}
df = pd.DataFrame(data)

# Преобразование данных в формат, подходящий для моделирования
X = df[['Year']]
y = df['WaterLevel']

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X, y)

# Предсказание уровня воды на предстоящий год (2023)
next_year = 2023
predicted_water_level = model.predict([[next_year]])

print(f"Предсказанное значение уровня воды в реке Batareyka River на {next_year}: {predicted_water_level[0]:.2f}")

# Визуализация данных и предсказания на карте с использованием folium
m = folium.Map(location=[54.3167, 83.0000], zoom_start=10)

folium.Marker([54.3167, 83.0000], popup=f"Предсказанное значение уровня воды: {predicted_water_level[0]:.2f}").add_to(m)

# Добавление точек с историческими данными
for index, row in df.iterrows():
    folium.Marker([54.3167, 83.0000], popup=f"Год: {row['Year']}, Уровень воды: {row['WaterLevel']:.2f}").add_to(m)

# Сохранение карты
m.save("55.html")