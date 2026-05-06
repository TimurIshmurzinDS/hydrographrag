import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('sarykan_river_data.csv')
X = data[['temperature', 'precipitation']]
y = data['discharge']

# Шаг 2: Преобразование данных
X_norm = (X - X.min()) / (X.max() - X.min())
y_norm = (y - y.min()) / (y.max() - y.min())

# Шаг 3: Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X_norm, y_norm, test_size=0.2)

# Шаг 4: Обучение модели
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 5: Проверка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Шаг 6: Прогнозирование стока на следующий сезон
next_season_data = pd.read_csv('next_season_data.csv')
X_next_season_norm = (next_season_data - X.min()) / (X.max() - X.min())
predicted_discharge = model.predict(X_next_season_norm) * (y.max() - y.min()) + y.min()

# Визуализация на карте
m = folium.Map(location=[51.0, 73.0], zoom_start=8)
folium.Marker([51.0, 73.0], popup='Сарыкан').add_to(m)
m.save("52.html")