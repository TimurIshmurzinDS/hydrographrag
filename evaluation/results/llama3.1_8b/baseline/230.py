import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import folium

# Сбор и обработка данных
data = pd.read_csv('ossek_river_data.csv')
eth_price = pd.read_csv('ethereum_price_data.csv')

# Объединение данных о стоке реки Осек и курсе Ethereum
merged_data = pd.merge(data, eth_price, on='date')

# Подготовка данных для моделирования
X = merged_data[['ossek_flow']]
y = merged_data['eth_price']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Выбор модели машинного обучения
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Тренировка модели на основе подготовленных данных
model.fit(X_train, y_train)

# Оценка качества модели с помощью метрик
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f'Коэффициент детерминации R^2: {r2}')

# Использование модели для предсказания курса Ethereum на основе стока реки Осек
predicted_eth_price = model.predict(pd.DataFrame({'ossek_flow': [100]}))

# Визуализация результатов на карте с помощью библиотеки Folium
m = folium.Map(location=[55.75, 37.62], zoom_start=10)
folium.Marker([55.75, 37.62], popup=f'Предсказанный курс Ethereum: {predicted_eth_price}').add_to(m)
m.save("230.html")