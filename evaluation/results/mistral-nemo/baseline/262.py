import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('oil_price_fish_population.csv')

# Шаг 2: Очистка данных
data.dropna(inplace=True)

# Шаг 3: Разделение данных
X_train, X_test, y_train, y_test = train_test_split(data[['oil_price']], data['fish_population'], test_size=0.2, random_state=42)

# Шаг 4: Создание модели
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 5: Обучение модели и оценка точности
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Шаг 6: Предсказание популяции рыб на основе текущих цен на нефть
current_oil_price = pd.DataFrame({'oil_price': [100]}) # Пример текущей цены на нефть
predicted_fish_population = model.predict(current_oil_price)
print(f'Predicted fish population: {predicted_fish_population[0]}')

# Визуализация данных на карте с использованием библиотеки folium
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13) # Пример местоположения реки Бутак

for index, row in data.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']],
                        radius=row['fish_population']/100,
                        color='blue',
                        fill=True).add_to(m)

m.save("262.html")