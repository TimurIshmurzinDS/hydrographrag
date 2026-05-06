import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import folium

# Загрузка данных (замените на ваши файлы)
data = pd.read_csv("fish_population_oil_prices.csv")

# Обработка данных (очистка, преобразование типов, создание lagged variables)
# ...

# Разделение данных на обучающий и тестовый набор
X = data[['oil_price']]
y = data['fish_population']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Обучение модели (линейная регрессия в данном примере)
model = LinearRegression()
model.fit(X_train, y_train)

# Предсказание на тестовом наборе
y_pred = model.predict(X_test)

# Оценка точности модели (например, R-squared)
from sklearn.metrics import r2_score
r2 = r2_score(y_test, y_pred)
print("R-squared:", r2)

# Предсказание на основе будущих цен на нефть
future_oil_prices = [ # ... введите будущие цены на нефть]
future_population = model.predict([[price]] for price in future_oil_prices)

# Визуализация (необязательно, но рекомендуется)
m = folium.Map(location=[45.6789, 32.1234], zoom_start=10) # Замените на координаты реки Бутак
folium.Marker([45.6789, 32.1234], popup="Predicted Fish Population: " + str(future_population[0])).add_to(m)

m.save("262.html")