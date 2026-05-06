import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('uzyn_kargaly_data.csv')

# Шаг 2: Очистка данных
data.dropna(inplace=True)

# Шаг 3: Анализ данных
X = data[['temperature', 'precipitation']]
y = data['water_level']

# Шаг 4: Построение модели
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 5: Тестирование модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Шаг 6: Визуализация результатов
m = folium.Map(location=[49.8397, 24.0297], zoom_start=12)

# Добавляем точки на карту в зависимости от уровня воды
for i in range(len(data)):
    if data.iloc[i]['water_level'] > 5:
        folium.CircleMarker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                            radius=5,
                            color='red',
                            fill=True).add_to(m)
    elif data.iloc[i]['water_level'] <= 5 and data.iloc[i]['water_level'] > 3:
        folium.CircleMarker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                            radius=5,
                            color='orange',
                            fill=True).add_to(m)
    else:
        folium.CircleMarker(location=[data.iloc[i]['latitude'], data.iloc[i]['longitude']],
                            radius=5,
                            color='green',
                            fill=True).add_to(m)

m.save("211.html")