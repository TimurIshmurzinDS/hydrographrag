import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import folium

# Шаг 1: Сбор данных
def fetch_crypto_data(symbol='BTC', vs_currency='usd'):
    url = f'https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency={vs_currency}&days=365&interval=daily'
    response = pd.read_json(url)
    prices_df = pd.DataFrame(response['prices'], columns=['timestamp', 'price'])
    prices_df['timestamp'] = pd.to_datetime(prices_df['timestamp'], unit='ms')
    return prices_df

# Шаг 2: Предобработка данных
def preprocess_data(df):
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)
    df.dropna(inplace=True)
    return df

# Шаг 3: Вычисление волатильности
def calculate_volatility(df, window=7):
    df['log_return'] = np.log(df['price']).diff()
    df[f'volatility_{window}d'] = df['log_return'].rolling(window=window).std()
    return df.dropna()

# Шаг 4: Формирование признаков
def create_features(df, window=7):
    for i in range(1, window+1):
        df[f'price_shift_{i}d'] = df['price'].shift(i)
    df.dropna(inplace=True)
    return df

# Шаг 5: Разделение данных
def split_data(df, test_size=0.2):
    X = df.drop(['price'], axis=1)
    y = df['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, shuffle=False)
    return X_train, X_test, y_train, y_test

# Шаг 6: Выбор модели
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Шаги 7-8: Обучение и оценка модели
def train_and_evaluate_model(X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    print(f'RMSE: {rmse}, MAE: {mae}')
    return y_pred

# Шаг 9: Предсказание
def predict_future(df, model, days=30):
    last_row = df.iloc[-1]
    predictions = []
    for _ in range(days):
        features = np.array([last_row[f'price_shift_{i}d'] for i in range(1, window+1)] + [last_row[f'volatility_{window}d']])
        predicted_price = model.predict(features.reshape(1, -1))[0]
        predictions.append(predicted_price)
        last_row = pd.Series([predicted_price] + list(last_row[:-2]) + [last_row[-1]])
    return predictions

# Шаг 10: Визуализация результатов
def visualize_results(df, y_pred):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['price'], label='Actual Price')
    plt.plot(df.index[-len(y_pred):], y_pred, label='Predicted Price', linestyle='--')
    plt.title('Crypto Price Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# Основной код
symbol = 'bitcoin'
window = 7

# Сбор и предобработка данных
crypto_data = fetch_crypto_data(symbol)
crypto_data = preprocess_data(crypto_data)

# Вычисление волатильности и формирование признаков
crypto_data = calculate_volatility(crypto_data, window=window)
crypto_data = create_features(crypto_data, window=window)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = split_data(crypto_data)

# Обучение модели и оценка точности
y_pred = train_and_evaluate_model(X_train, X_test, y_train, y_test)

# Визуализация результатов
visualize_results(crypto_data[-len(y_test):], y_pred)

# Предсказание будущих цен
future_predictions = predict_future(crypto_data.iloc[-window:], model, days=30)
print(f'Future Predictions: {future_predictions}')

# Создание карты с использованием folium (пример для демонстрации)
m = folium.Map(location=[55.7558, 37.6173], zoom_start=12)  # Координаты Москвы
folium.Marker([55.7558, 37.6173], popup='Moscow').add_to(m)
m.save("282.html")