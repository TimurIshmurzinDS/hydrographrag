import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import folium

# 1. Загрузка данных (замените на ваши файлы)
data = pd.read_csv("sarykan_flow_data.csv")
weather_data = pd.read_csv("sarykan_weather_data.csv")

# 2. Обработка данных (проведите анализ и очистку)
# ...

# 3. Выбор модели (здесь используется линейная регрессия)
model = LinearRegression()

# 4. Обучение модели
X = weather_data[['precipitation', 'temperature']]  # Выберите релевантные признаки
y = data['flow']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model.fit(X_train, y_train)

# 5. Оценка модели
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred, squared=False)
print("R-squared:", r2)
print("RMSE:", rmse)

# 6. Прогнозирование (используйте прогнозы метеорологических данных на следующий сезон)
future_weather = pd.DataFrame({'precipitation': [10], 'temperature': [5]})  # Пример
predicted_flow = model.predict(future_weather)
print("Predicted flow:", predicted_flow)

# Визуализация (пример, замените координаты на реальные)
m = folium.Map(location=[42.87, 79.05], zoom_start=10)
folium.Marker([42.87, 79.05], popup="Sarykan River").add_to(m)

# Сохранение карты
m.save("52.html")