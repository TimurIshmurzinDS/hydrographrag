import pandas as pd
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import folium

# Загрузка данных
data = pd.read_csv('water_access_data.csv')

# Предположим, что данные содержат следующие столбцы:
# 'date', 'flow_rate', 'precipitation', 'temperature', 'water_level', 'accessibility'

# Преобразование даты в формат datetime
data['date'] = pd.to_datetime(data['date'])

# Создание признаков и целевой переменной
X = data[['flow_rate', 'precipitation', 'temperature', 'water_level']]
y = data['accessibility']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели линейной регрессии
model = LinearRegression()
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка производительности модели
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Визуализация результатов на карте
# Предположим, что у нас есть геоданные о местоположении точек доступности воды
gdf = gpd.read_file('water_access_locations.shp')

# Создание карты
m = folium.Map(location=[gdf['latitude'].mean(), gdf['longitude'].mean()], zoom_start=10)

# Добавление маркеров с прогнозами доступности воды
for idx, row in gdf.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f'Прогноз доступности: {y_pred[idx]:.2f}',
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("206.html")