import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
import folium

# Шаг 1: Сбор данных
# Предположим, что у нас есть два файла CSV: 'discharge_data.csv' и 'agro_ecosystems_data.csv'
# discharge_data.csv содержит данные о стоке реки Бутак (дата, сток)
# agro_ecosystems_data.csv содержит данные об агроценозах (широта, долгота, устойчивость)

discharge_df = pd.read_csv('discharge_data.csv', parse_dates=['date'])
agro_ecosystems_df = pd.read_csv('agro_ecosystems_data.csv')

# Шаг 2: Предобработка данных
discharge_df.dropna(inplace=True)
discharge_df.set_index('date', inplace=True)

# Нормализация временных рядов (если необходимо)
discharge_df['discharge'] = (discharge_df['discharge'] - discharge_df['discharge'].mean()) / discharge_df['discharge'].std()

# Шаг 3: Анализ сезонных колебаний
result = seasonal_decompose(discharge_df['discharge'], model='additive')
seasonal_component = result.seasonal

# Шаг 4: Моделирование влияния
# Предположим, что устойчивость агроценозов зависит от среднего стока за сезон
mean_discharge_by_month = discharge_df.resample('M').mean()

# Создаем новый DataFrame для обучения модели
model_data = pd.DataFrame({
    'month': mean_discharge_by_month.index.month,
    'discharge': mean_discharge_by_month['discharge']
})

# Предположим, что у нас есть данные об устойчивости агроценозов за каждый месяц
# Для примера создадим случайные данные о устойчивости
np.random.seed(0)
model_data['stability'] = np.random.rand(len(model_data)) * 10

# Обучение модели линейной регрессии
X = model_data[['month', 'discharge']]
y = model_data['stability']
regressor = LinearRegression()
regressor.fit(X, y)

# Предсказание устойчивости агроценозов на основе стока реки
model_data['predicted_stability'] = regressor.predict(X)

# Шаг 5: Визуализация результатов
m = folium.Map(location=[agro_ecosystems_df['latitude'].mean(), agro_ecosystems_df['longitude'].mean()], zoom_start=10)

for _, row in agro_ecosystems_df.iterrows():
    folium.CircleMarker(
        location=(row['latitude'], row['longitude']),
        radius=row['stability'] * 2,  # Увеличиваем радиус для лучшей видимости
        color='blue',
        fill=True,
        fill_color='blue'
    ).add_to(m)

m.save("192.html")