import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
import folium

# Функция для получения данных о курсе биткоина
def get_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data['bitcoin']['usd']

# Функция для получения данных о уровне воды в реке Эмел
def get_water_level_data():
    # Здесь нужно будет реализовать логику для получения данных о уровне воды
    # Например, можно использовать API или данные из базы данных
    water_levels = [100, 95, 90, 85, 80]  # Пример данных
    return water_levels

# Получение данных
bitcoin_price = get_bitcoin_data()
water_levels = get_water_level_data()

# Создание DataFrame для анализа
data = pd.DataFrame({
    'Water_Level': water_levels,
    'Bitcoin_Price': [bitcoin_price] * len(water_levels)
})

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(data[['Water_Level']], data['Bitcoin_Price'])

# Предсказание курса биткоина при уменьшении уровня воды
new_water_level = 75
predicted_bitcoin_price = model.predict([[new_water_level]])

print(f"Предсказанный курс биткоина при уровне воды {new_water_level}: ${predicted_bitcoin_price[0]:.2f}")

# Визуализация на карте с использованием folium
m = folium.Map(location=[54.3167, 48.3333], zoom_start=10)

folium.Marker(
    location=[54.3167, 48.3333],
    popup=f"Уровень воды: {new_water_level}<br>Предсказанный курс биткоина: ${predicted_bitcoin_price[0]:.2f}",
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

m.save("258.html")