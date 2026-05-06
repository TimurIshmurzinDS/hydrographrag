import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных о стоке реки Kurty River и Шарынской реки
kurty_data = pd.read_csv('kurty_river.csv')
sharyn_data = pd.read_csv('sharyn_river.csv')

# Объединение данных для анализа
data = pd.merge(kurty_data, sharyn_data, on='date', how='inner')

# Удаление пропусков и аномалий
data.dropna(inplace=True)
data = data[(data['flow_kurty'] > 0) & (data['flow_sharyn'] > 0)]

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data[['flow_kurty', 'flow_sharyn']], data['flow_sharyn'], test_size=0.2, random_state=42)

# Создание линейной регрессии для предсказания стока Шарынской реки
model = LinearRegression()
model.fit(X_train, y_train)

# Оценка качества модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Коэффициент детерминации: {model.score(X_test, y_test)}')
print(f'MSE: {mse}')

# Визуализация результатов на карте с помощью библиотеки Folium
m = folium.Map(location=[43.5, 76.0], zoom_start=10)
folium.Marker([43.5, 76.0], popup='Курты-Рык').add_to(m)
folium.Marker([44.2, 75.8], popup='Шарын').add_to(m)

# Визуализация данных на карте
for i in range(len(data)):
    folium.CircleMarker([data['lat_kurty'].iloc[i], data['lon_kurty'].iloc[i]], radius=5).add_to(m)
    folium.CircleMarker([data['lat_sharyn'].iloc[i], data['lon_sharyn'].iloc[i]], radius=5).add_to(m)

# Сохранение карты в файл
m.save("123.html")