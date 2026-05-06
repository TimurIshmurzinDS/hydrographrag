import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import folium

# Сбор данных (предполагается, что данные хранятся в DataFrame)
data = pd.DataFrame({
    'water_level': [1.2, 2.3, 3.4, 4.5, 5.6],
    'token_price': [10.0, 20.0, 30.0, 40.0, 50.0]
})

# Предобработка данных
data['water_level'] = data['water_level'].astype(float)
data['token_price'] = data['token_price'].astype(float)

# Разделение данных на обучающую и тестовую выборки
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Обучение модели
model = LinearRegression()
model.fit(train_data[['water_level']], train_data['token_price'])

# Оценка модели
y_pred = model.predict(test_data[['water_level']])
print(f'Коэффициент determination (R^2): {r2_score(test_data["token_price"], y_pred)}')
print(f'Средняя абсолютная ошибка (MAE): {mean_absolute_error(test_data["token_price"], y_pred)}')

# Визуализация результатов на карте
m = folium.Map(location=[51.5, 72.0], zoom_start=10)
folium.Marker([51.5, 72.0], popup='Река Баянколь').add_to(m)
folium.PolyLine([[51.4, 71.9], [51.6, 72.1]], color='red', weight=2).add_to(m)

# Прогноз стоимости токенов на основе уровня воды в реке Баянколь
water_level = 3.5
token_price = model.predict([[water_level]])
print(f'Прогноз стоимости токенов на уровне воды {water_level}: {token_price[0]}')

# Сохранение карты
m.save("264.html")