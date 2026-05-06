import pandas as pd
import numpy as np
import folium
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# 1. Генерация синтетических данных
np.random.seed(42)
dates = pd.date_range(start="2023-01-01", periods=200)

# Курс Биткоина (имитация случайного блуждания)
btc_price = 30000 + np.cumsum(np.random.randn(200) * 1000)

# Уровень воды в реке Batareyka (имитация сезонности + шум)
# Уровень воды колеблется от 1.0 до 5.0 метров
water_level = 3.0 + 1.5 * np.sin(np.linspace(0, 4 * np.pi, 200)) + np.random.randn(200) * 0.5

df = pd.DataFrame({'date': dates, 'btc': btc_price, 'water_level': water_level})

# 2. Инженерия признаков (создание лагов для BTC)
# Мы создаем признаки: цена BTC сегодня, вчера и 3 дня назад
df['btc_lag1'] = df['btc'].shift(1)
df['btc_lag3'] = df['btc'].shift(3)
df = df.dropna()

# 3. Подготовка данных для ML
X = df[['btc', 'btc_lag1', 'btc_lag3']]
y = df['water_level']

# Масштабирование признаков
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 4. Обучение модели Random Forest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогноз
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"Model Performance:\nMean Squared Error: {mse:.4f}\nR2 Score: {r2:.4f}")

# 5. Геопространственная визуализация
# Предположим координаты реки Batareyka (условные координаты)
lat, lon = 48.5, 35.2 

# Создание карты
m = folium.Map(location=[lat, lon], zoom_start=12, tiles='OpenStreetMap')

# Добавление маркера с информацией о последнем прогнозе
last_pred = predictions[-1]
info_text = (f"Batareyka River Station<br>"
             f"Predicted Water Level: {last_pred:.2f}m<br>"
             f"Based on BTC Correlation Model")

folium.Marker(
    [lat, lon], 
    popup=info_text, 
    tooltip="Water Level Prediction",
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# Добавление круга, имитирующего зону влияния/мониторинга
folium.Circle(
    radius=5000, 
    location=[lat, lon], 
    color='blue', 
    fill=True, 
    fill_opacity=0.2
).add_to(m)

# Сохранение карты
m.save("212.html")
print("Map has been saved as 212.html")