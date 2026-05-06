import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import folium

# Загрузка исторических данных о стоке реки Аксу
data = pd.read_csv('aksu_river_data.csv')

# Подготовка данных для обучения модели
X = data.drop(['сток'], axis=1)
y = data['сток']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели прогнозирования пиковых паводков
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка точности модели
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f'Точность модели: {mae:.2f}')

# Прогнозирование пиковых паводков для следующего сезона
next_season_data = pd.DataFrame({'параметр1': [10, 20, 30], 'параметр2': [40, 50, 60]})
next_season_pred = model.predict(next_season_data)

# Визуализация результатов на карте с помощью библиотеки Folium
m = folium.Map(location=[45.0, 75.0], zoom_start=10)
folium.Marker([45.0, 75.0], popup='Пиковый паводок').add_to(m)
folium.Marker([46.0, 76.0], popup='Низкий сток').add_to(m)

# Добавление инфо-окна с подробной информацией о прогнозах и рисках
infowindow = folium.Div(
    'Прогноз пикового паводка: {:.2f} м³/сек. Риск: {:.2f}%'.format(next_season_pred[0], 10),
    width=200, height=100
)
folium.Marker([47.0, 77.0], popup=infowindow).add_to(m)

# Сохранение карты в файл
m.save('197.html')