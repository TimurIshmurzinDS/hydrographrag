import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import folium

# Предположим, что у нас есть два файла: 'historical_flow_data.csv' и 'irrigation_demand_data.csv'
# historical_flow_data.csv содержит столбцы: date, flow_rate (куб. м/с)
# irrigation_demand_data.csv содержит столбцы: date, demand (куб. м)

# Загрузка данных
flow_data = pd.read_csv('historical_flow_data.csv', parse_dates=['date'])
demand_data = pd.read_csv('irrigation_demand_data.csv', parse_dates=['date'])

# Объединение данных по дате
data = pd.merge(flow_data, demand_data, on='date')

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(data[['flow_rate']], data['demand'], test_size=0.2, random_state=42)

# Обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
mse = mean_squared_error(y_test, y_pred)
print(f'Средняя квадратическая ошибка: {mse}')

# Прогноз потребности в воде для будущих дат на основе исторических данных о стоках
future_dates = pd.date_range(start=data['date'].max() + pd.Timedelta(days=1), periods=30)
future_flow_rates = np.random.uniform(low=data['flow_rate'].min(), high=data['flow_rate'].max(), size=len(future_dates))
future_data = pd.DataFrame({'date': future_dates, 'flow_rate': future_flow_rates})
future_demand_pred = model.predict(future_data[['flow_rate']])
future_data['predicted_demand'] = future_demand_pred

# Визуализация на карте с использованием folium
# Предположим, что у нас есть координаты бассейна реки Токыраун
m = folium.Map(location=[42.8746, 74.5910], zoom_start=10)  # Координаты примерные

# Добавление маркеров с прогнозируемой потребностью в воде
for _, row in future_data.iterrows():
    folium.Marker(
        location=[42.8746, 74.5910],  # Координаты примерные
        popup=f"Date: {row['date'].strftime('%Y-%m-%d')}, Predicted Demand: {row['predicted_demand']:.2f} куб. м",
    ).add_to(m)

# Сохранение карты в файл
m.save("193.html")