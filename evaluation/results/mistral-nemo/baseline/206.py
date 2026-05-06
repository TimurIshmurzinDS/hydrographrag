import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import folium

# Шаг 1: Сбор данных
data = pd.read_csv('water_availability_data.csv')

# Шаг 2: Предобработка данных
data = data.drop_duplicates()
data = data.fillna(method='ffill')
data = (data - data.min()) / (data.max() - data.min())

# Шаг 3: Выбор метода моделирования
X = data.drop('water_availability', axis=1)
y = data['water_availability']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Шаг 4: Обучение модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Шаг 5: Прогнозирование доступности воды
future_data = pd.read_csv('future_factors.csv')
predictions = model.predict(future_data)

# Шаг 6: Визуализация результатов
map_osm = folium.Map(location=[43.2, 76.9], zoom_start=8)
for index, row in data.iterrows():
    lat, lon = row['latitude'], row['longitude']
    availability = row['water_availability']
    popup_text = f'Water Availability: {availability}'
    folium.CircleMarker(location=[lat, lon], radius=5, color='blue', fill=True).add_to(map_osm)
map_osm.save("206.html")