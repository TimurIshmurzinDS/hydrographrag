import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import folium

# Загрузим данные о стоке для рек Byzhy и Urzhar
byzhy_data = pd.read_csv('byzhy_stok.csv')
urzhar_data = pd.read_csv('urzhar_stok.csv')

# Объединим данные в одну таблицу с индексом времени
data = pd.concat([byzhy_data, urzhar_data], keys=['Byzhy', 'Urzhar'])
data.reset_index(level=0, inplace=True)

# Разделим данные на обучающую и тестовую выборки (80% для обучения)
X_train, X_test, y_train, y_test = train_test_split(data.drop('сток', axis=1), data['сток'], test_size=0.2, random_state=42)

# Создадим модель линейной регрессии
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

# Оценим качество модели линейной регрессии
r2_score_lr = r2_score(y_test, y_pred_lr)
mse_lr = mean_squared_error(y_test, y_pred_lr)
print(f'Коэффициент детерминации R² для модели линейной регрессии: {r2_score_lr:.3f}')
print(f'Оценка ошибки среднеквадратичная для модели линейной регрессии: {mse_lr:.3f}')

# Создадим модель случайного леса
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

# Оценим качество модели случайного леса
r2_score_rf = r2_score(y_test, y_pred_rf)
mse_rf = mean_squared_error(y_test, y_pred_rf)
print(f'Коэффициент детерминации R² для модели случайного леса: {r2_score_rf:.3f}')
print(f'Оценка ошибки среднеквадратичная для модели случайного леса: {mse_rf:.3f}')

# Сравним результаты моделей
if r2_score_lr > r2_score_rf:
    print('Модель линейной регрессии лучше подходит для прогнозирования стока.')
else:
    print('Модель случайного леса лучше подходит для прогнозирования стока.')

# Создадим визуализацию на карте с помощью библиотеки Folium
m = folium.Map(location=[50.0, 70.0], zoom_start=6)
folium.Marker([byzhy_data['широта'].mean(), byzhy_data['долгота'].mean()], popup='Byzhy River').add_to(m)
folium.Marker([urzhar_data['широта'].mean(), urzhar_data['долгота'].mean()], popup='Urzhar River').add_to(m)
m.save('204.html')