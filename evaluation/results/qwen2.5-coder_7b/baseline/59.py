import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Загрузка исторических данных о погоде и расходе воды в реке Shilik River
data = pd.read_csv('shilik_river_data.csv')

# Предположим, что данные содержат следующие столбцы:
# 'date', 'precipitation', 'temperature', 'flow_rate'

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Создание признаков и целевой переменной
X = data[['precipitation', 'temperature']]
y = data['flow_rate']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Визуализация результатов на карте
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)

for index, row in data.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=f"Flow Rate: {row['flow_rate']}, Precipitation: {row['precipitation']}, Temperature: {row['temperature']}").add_to(m)

m.save("59.html")