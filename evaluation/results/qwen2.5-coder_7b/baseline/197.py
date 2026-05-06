import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Загрузка данных
data = pd.read_csv('aksu_river_data.csv')

# Предположим, что данные содержат столбец 'date' и 'flow'
data['date'] = pd.to_datetime(data['date'])
data.set_index('date', inplace=True)

# Проверка на пропущенные значения
print("Пропущенные значения:", data.isnull().sum())

# Устранение пропущенных значений (например, заполнение средними)
data.fillna(method='ffill', inplace=True)

# Разделение данных на обучающую и тестовую выборки
train_data = data.iloc[:-30]  # Последние 30 дней для тестирования
test_data = data.iloc[-30:]

# Выбор признаков и целевой переменной
X_train = train_data.drop(columns=['flow'])
y_train = train_data['flow']
X_test = test_data.drop(columns=['flow'])
y_test = test_data['flow']

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Среднеквадратичная ошибка: {mse}")
print(f"R^2: {r2}")

# Прогнозирование на следующий сезон (предположим, что у нас есть данные для следующих 30 дней)
next_season_data = pd.DataFrame(index=pd.date_range(start='2024-01-01', periods=30))
y_pred_next_season = model.predict(next_season_data)

# Визуализация результатов
m = folium.Map(location=[data.index[-1].latitude, data.index[-1].longitude], zoom_start=10)
folium.PolyLine(locations=data[['latitude', 'longitude']].values.tolist(), color='blue').add_to(m)

for date, flow in zip(data.index, data['flow']):
    folium.Marker([date.latitude, date.longitude], popup=f"Flow: {flow}").add_to(m)

for date, pred_flow in zip(next_season_data.index, y_pred_next_season):
    folium.Marker([date.latitude, date.longitude], popup=f"Predicted Flow: {pred_flow}", icon=folium.Icon(color='red')).add_to(m)

m.save("197.html")