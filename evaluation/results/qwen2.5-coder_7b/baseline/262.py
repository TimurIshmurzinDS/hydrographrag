import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Загрузка данных
data = {
    'price_of_oil': [50, 60, 70, 80, 90],  # Примерные данные по цене на нефть
    'fish_population': [1000, 1200, 1400, 1600, 1800]  # Примерные данные по популяции рыб
}
df = pd.DataFrame(data)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(df[['price_of_oil']], df['fish_population'], test_size=0.2, random_state=42)

# Создание модели линейной регрессии
model = LinearRegression()

# Обучение модели
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Визуализация данных и прогноза на карте с использованием folium
m = folium.Map(location=[50.4501, 30.5234], zoom_start=13)  # Примерные координаты Бутака

# Добавление точек для реальных данных
for idx, row in df.iterrows():
    folium.Marker([50.4501 + idx * 0.01, 30.5234 + idx * 0.01], popup=f"Price: {row['price_of_oil']}, Population: {row['fish_population']}").add_to(m)

# Добавление точек для прогнозов
for idx, pred in enumerate(y_pred):
    folium.Marker([50.4501 + (len(df) + idx) * 0.01, 30.5234 + (len(df) + idx) * 0.01], popup=f"Predicted Population: {pred}").add_to(m)

# Сохранение карты
m.save("262.html")