import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import folium

# Сбор и обработка данных
data = pd.read_csv('cryptocurrency_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)
data['Volatility'] = data['Close'].pct_change()

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Моделирование волатильности с помощью случайного леса
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(train_data[['Open', 'High', 'Low', 'Close', 'Volume']], train_data['Volatility'])

# Предсказание волатильности на тестовой выборке
test_pred_volatility = rf_model.predict(test_data[['Open', 'High', 'Low', 'Close', 'Volume']])

# Предсказание падения стоимости криптовалюты
test_pred_price_change = test_data['Close'].pct_change()

# Оценка точности модели
mse = mean_squared_error(test_pred_volatility, test_data['Volatility'])
print(f'MSE: {mse}')

# Визуализация результатов на карте с помощью Folium
m = folium.Map(location=[37.7749, -122.4194], zoom_start=13)
folium.Marker([37.7858, -122.4364], popup='Падение стоимости криптовалюты').add_to(m)

# Добавление данных о волатильности и падении стоимости на карту
for i in range(len(test_data)):
    folium.CircleMarker(
        location=[37.7858 + test_pred_volatility[i] * 0.01, -122.4364],
        radius=10,
        color='red',
        popup=f'Волатильность: {test_pred_volatility[i]:.2f}, Падение стоимости: {test_pred_price_change[i]:.2f}'
    ).add_to(m)

# Сохранение карты в файл
m.save("282.html")