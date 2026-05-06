import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных о сезонных колебаниях уровня воды в реке Каскелен.
data = {
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'water_level': [100, 120, 150, 180, 200, 220, 250, 280, 300, 320, 350, 380]
}

df = pd.DataFrame(data)

# Шаг 2: Анализ данных и выявление закономерностей в зависимости от времени года.
print(df.describe())

# Шаг 3: Создание модели, которая связывает уровень воды в реке с процессом выпечки хлеба.
X = df[['month']]
y = df['water_level']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 4: Визуализация результатов на карте.
m = folium.Map(location=[50.05, 78.5], zoom_start=10)
folium.Marker([50.05, 78.5], popup='Оптимальное время выпечки хлеба').add_to(m)

# Добавление данных о сезонных колебаниях уровня воды в реке Каскелен.
for i in range(len(df)):
    folium.CircleMarker(
        location=[df['month'][i] * 0.1, df['water_level'][i]],
        radius=10,
        color='red',
        popup=f'Месяц: {df["month"][i]}, Уровень воды: {df["water_level"][i]}'
    ).add_to(m)

m.save("240.html")