import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Шаг 1: Подготовка данных
data = pd.read_csv('solar_flares_data.csv')

# Шаг 2: Преобразование данных
data['days_from_start'] = (data['date'] - data['date'].min()).dt.days

# Шаг 3: Выбор признаков
X = data[['days_from_start', 'maxwell_number', 'kp_index', ...]]  # Добавить другие параметры активности Солнца
y = data['flares_intensity']

# Шаг 4: Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Шаг 5: Построение модели регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Шаг 6: Оценка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f'Mean Squared Error: {mse}')
print(f'R-squared Score: {r2}')

# Шаг 7: Визуализация результатов
map_flares = folium.Map(location=[0, 0], zoom_start=2)

for index, row in data.iterrows():
    if row['latitude'] is not None and row['longitude'] is not None:
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=row['flares_intensity'],
            color='red',
            fill=True,
            fill_opacity=0.5
        ).add_to(map_flares)

map_flares.save("275.html")