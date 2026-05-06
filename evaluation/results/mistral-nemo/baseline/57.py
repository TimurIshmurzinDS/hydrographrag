import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import folium

# 1. Подготовка данных
data = pd.read_csv('kurty_river_water_level.csv')
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# 2. Преобразование данных
data['days_since_start'] = (data.index - data.index.min()).days

# 3. Разделение данных
X_train, X_test, y_train, y_test = train_test_split(data[['days_since_start']], data['water_level'], test_size=0.2, random_state=42)

# 4. Моделирование
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Оценка модели
y_pred = model.predict(X_test)
print(f'MAE: {mean_absolute_error(y_test, y_pred)}')
print(f'R²: {r2_score(y_test, y_pred)}')

# 6. Прогнозирование
future_dates = pd.date_range(start=data.index.max(), periods=365*5)
future_days_since_start = (future_dates - future_dates.min()).days
predictions = model.predict(future_days_since_start.reshape(-1, 1))

# 7. Визуализация
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=8)

for idx, row in data.iterrows():
    folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, fill=True, color='blue', fill_opacity=0.7).add_to(m)
    folium.Marker([row['latitude'], row['longitude']], popup=f'Дата: {idx}\nУровень воды: {row["water_level"]} м').add_to(m)

for idx, pred in enumerate(predictions):
    folium.CircleMarker(location=[data.iloc[-1]['latitude'], data.iloc[-1]['longitude'] + (idx / 365) * 0.1], radius=5, fill=True, color='red', fill_opacity=0.7).add_to(m)
    folium.Marker([data.iloc[-1]['latitude'], data.iloc[-1]['longitude'] + (idx / 365) * 0.1], popup=f'Дата: {future_dates[idx]}\nПрогнозируемый уровень воды: {pred:.2f} м').add_to(m)

m.save("57.html")