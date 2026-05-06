import pandas as pd
import numpy as np
import folium
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
from math import radians, cos, sin, asin, sqrt

# 1. Генерация синтетических данных (имитация реального датасета)
np.random.seed(42)
n_samples = 200

# Центр города (например, Москва)
city_center = (55.7558, 37.6173)

data = {
    'lat': np.random.uniform(55.60, 55.90, n_samples),
    'lon': np.random.uniform(37.40, 37.80, n_samples),
    'area': np.random.uniform(30, 150, n_samples),
    'rooms': np.random.randint(1, 5, n_samples),
}

df = pd.DataFrame(data)

# Функция для расчета расстояния (Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Радиус Земли в км
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dlambda/2)**2
    return 2 * R * asin(sqrt(a))

# Добавляем признак: расстояние до центра
df['dist_to_center'] = df.apply(lambda row: haversine(row['lat'], row['lon'], city_center[0], city_center[1]), axis=1)

# Создаем целевую переменную 'price' с зависимостью от площади и расстояния до центра
# Цена = (Площадь * 100к) - (Расстояние * 50к) + шум
df['price'] = (df['area'] * 100000) - (df['dist_to_center'] * 500000) + np.random.normal(0, 500000, n_samples)
df['price'] = df['price'].clip(lower=2000000) # Минимальная цена 2 млн

# 2. Подготовка к моделированию
X = df[['lat', 'lon', 'area', 'rooms', 'dist_to_center']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 3. Обучение модели регрессии
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Предсказания
y_pred = model.predict(X_test_scaled)

# Оценка
print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")

# 4. Визуализация на карте
# Создаем карту, центрированную в городе
m = folium.Map(location=city_center, zoom_start=11, tiles='CartoDB positron')

# Функция для определения цвета в зависимости от цены
def get_color(price):
    if price > 12000000: return 'red'
    if price > 7000000: return 'orange'
    if price > 4000000: return 'yellow'
    return 'green'

# Добавляем все объекты из тестовой выборки на карту
test_indices = X_test.index
for idx in test_indices:
    row = df.loc[idx]
    # Получаем предсказанную цену для этого объекта
    scaled_features = scaler.transform([X.loc[idx]])
    pred_price = model.predict(scaled_features)[0]
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=6,
        popup=f"Price: {pred_price:,.0f} руб.<br>Area: {row['area']:.1f} m2",
        color=get_color(pred_price),
        fill=True,
        fill_color=get_color(pred_price),
        fill_opacity=0.7
    ).add_to(m)

# Сохранение карты
m.save("279.html")
print("Map has been saved as 279.html")