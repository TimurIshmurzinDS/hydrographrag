import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('dos_river_sensor_data.csv')
ethereum_price_data = pd.read_csv('ethereum_price_data.csv')

# Шаг 2: Очистка данных
data = data.dropna()
ethereum_price_data = ethereum_price_data.dropna()

# Шаг 3: Преобразование данных
X = data[['dos_river_sensor_1', 'dos_river_sensor_2', 'dos_river_sensor_3']]
y = ethereum_price_data['ethereum_price']

# Шаг 4: Обучение модели
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 5: Проверка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Шаг 6: Прогнозирование цен
current_sensor_data = pd.read_csv('current_dos_river_sensor_data.csv')
predicted_ethereum_price = model.predict(current_sensor_data)

# Шаг 7: Визуализация результатов
map = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
for index, row in predicted_ethereum_price.iterrows():
    lat = row['latitude']
    lon = row['longitude']
    price = row['predicted_ethereum_price']
    folium.CircleMarker(location=[lat, lon], radius=5, color='blue', fill=True).add_to(map)
map.save("213.html")