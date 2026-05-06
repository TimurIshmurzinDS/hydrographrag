import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import folium

# Загрузка данных
df = pd.read_csv('sarykan_river_data.csv')

# Изучение данных и выбор переменных
X = df[['осадки', 'температура_воздуха']]
y = df['сток']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка эффективности модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Среднеквадратическая ошибка: {mse}')

# Визуализация результатов на карте
m = folium.Map(location=[42.5, 77], zoom_start=10)
folium.Choropleth(
    geo_data='sarykan_river_map.geojson',
    data=df,
    columns=['сток'],
    key_on='feature.properties.name',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2
).add_to(m)
m.save('52.html')