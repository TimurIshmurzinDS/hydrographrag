import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from folium import Map, Marker

# Сбор и обработка данных
data = {
    'water_level': [10, 12, 15, 18, 20],  # Уровень воды в реке Эмел (м)
    'bitcoin_price': [50000, 52000, 55000, 58000, 60000]  # Курс биткоина
}
df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df[['water_level']], df['bitcoin_price'], test_size=0.2, random_state=42)

# Создание модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозирование изменения курса биткоина
new_water_level = 12  # Новый уровень воды в реке Эмел (м)
new_bitcoin_price = model.predict([[new_water_level]])

print(f'Изменение курса биткоина: {new_bitcoin_price[0]}')

# Визуализация на карте
m = Map(location=[55.7558, 37.6173], zoom_start=10)  # Карта Москвы
Marker(location=[55.7558, 37.6173], popup='Новый уровень воды в реке Эмел: ' + str(new_water_level)).add_to(m)
m.save("258.html")