import pandas as pd
import folium
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Загрузка данных
data = pd.read_csv('temirlik_river_data.csv')

# Предположим, что данные содержат следующие столбцы:
# 'latitude', 'longitude' - координаты поста
# 'water_flow' - расход воды
# 'flood_probability' - вероятность наводнения (целевая переменная)

# Проверка данных
print(data.head())

# Разделение данных на обучающую и тестовую выборки
X = data[['latitude', 'longitude', 'water_flow']]
y = data['flood_probability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Визуализация данных на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Water Flow: {row['water_flow']}, Flood Probability: {row['flood_probability']:.2f}",
        icon=folium.Icon(color='blue' if row['flood_probability'] < 0.5 else 'red')
    ).add_to(m)

# Сохранение карты
m.save("78.html")