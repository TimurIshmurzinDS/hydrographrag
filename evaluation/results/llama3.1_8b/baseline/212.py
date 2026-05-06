import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Сбор и предобработка данных
data = {
    'water_level': [1.2, 1.5, 1.8, 2.0, 1.9, 1.7, 1.6, 1.4, 1.3],
    'bitcoin_price': [50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000]
}
df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df[['bitcoin_price']], df['water_level'], test_size=0.2, random_state=42)

# Выбор модели
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Тренировка модели
model.fit(X_train, y_train)

# Прогнозирование уровня воды на основе текущего курса биткоина
current_bitcoin_price = 85000
predicted_water_level = model.predict([[current_bitcoin_price]])

# Визуализация результатов на карте
m = Map(location=[55.7558, 37.6173], zoom_start=12)
Marker(location=[55.7558, 37.6173], popup=f'Прогнозированный уровень воды: {predicted_water_level[0]}').add_to(m)
m.save("212.html")