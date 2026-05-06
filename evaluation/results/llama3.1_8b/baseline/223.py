import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from folium import Map, Marker

# Загрузите данные о текущем уровне воды в реке Баянколь и цене золота на рынке.
data = {
    'water_level': [10, 12, 15, 18, 20],
    'gold_price': [1500, 1550, 1600, 1650, 1700]
}
df = pd.DataFrame(data)

# Разделите данные на обучающую и тестовую выборки.
X_train, X_test, y_train, y_test = train_test_split(df['water_level'], df['gold_price'], test_size=0.2, random_state=42)

# Создайте модель регрессии.
model = LinearRegression()

# Обучите модель на обучающей выборке.
model.fit(X_train.values.reshape(-1, 1), y_train.values)

# Сделайте предсказание цены золота на основе текущего уровня воды в реке Баянколь.
water_level = 16
predicted_gold_price = model.predict([[water_level]])

# Создайте карту с маркером для отображения текущего уровня воды и предсказанной цены золота.
m = Map(location=[50.0, 90.0], zoom_start=6)
Marker(location=[50.0, 90.0], popup=f'Текущий уровень воды: {water_level} м\nПредсказанная цена золота: {predicted_gold_price[0]} долларов').add_to(m)

# Сохраните карту в файл.
m.save("223.html")