import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть CSV файл с историческими данными о солнечных вспышках
data = pd.read_csv('solar_flare_data.csv', parse_dates=['date'], index_col='date')

# Шаг 2: Предобработка данных
# Нормализация данных
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['flare_count'].values.reshape(-1, 1))

# Создание набора данных для обучения LSTM
def create_dataset(dataset, time_step=1):
    dataX, dataY = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        dataX.append(a)
        dataY.append(dataset[i + time_step, 0])
    return np.array(dataX), np.array(dataY)

time_step = 6
X, y = create_dataset(scaled_data, time_step)
X = X.reshape(X.shape[0], X.shape[1], 1)

# Разделение данных на обучающую и тестовую выборки
train_size = int(len(X) * 0.8)
test_size = len(X) - train_size
X_train, X_test = X[0:train_size], X[train_size:len(X)]
y_train, y_test = y[0:train_size], y[train_size:len(y)]

# Шаг 3 и 4: Выбор модели и обучение
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=64, verbose=1)

# Шаг 5: Валидация модели
train_predict = model.predict(X_train)
test_predict = model.predict(X_test)

# Обратное преобразование нормализованных данных
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)
y_train = scaler.inverse_transform([y_train])
y_test = scaler.inverse_transform([y_test])

# Шаг 6: Предсказание и визуализация
future_days = 30
x_input = scaled_data[-time_step:].reshape(1, -1, 1)
lst_output = []
n_steps = time_step
i = 0

while(i < future_days):
    yhat = model.predict(x_input, verbose=0)
    lst_output.append(yhat[0][0])
    x_input = np.append(x_input[:, 1:, :], [[yhat]], axis=1)
    i += 1

future_predict = scaler.inverse_transform(np.array(lst_output).reshape(-1, 1))

# Визуализация предсказаний
plt.figure(figsize=(14,5))
plt.plot(data.index[-len(y_test):], y_test[0], label='Actual')
plt.plot(data.index[-len(test_predict):], test_predict, label='Predicted')
plt.plot(pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=future_days), future_predict, label='Future Predictions', linestyle='--')
plt.title('Предсказание солнечных вспышек')
plt.xlabel('Дата')
plt.ylabel('Количество вспышек')
plt.legend()
plt.show()

# Шаг 7: Визуализация на карте (пример)
# Предположим, что у нас есть координаты наблюдательной станции
m = folium.Map(location=[50.4319, 30.5151], zoom_start=2)  # Координаты Киева для примера

folium.Marker(
    location=[50.4319, 30.5151],
    popup='Пример наблюдательной станции',
    icon=folium.Icon(color='red')
).add_to(m)

m.save("275.html")