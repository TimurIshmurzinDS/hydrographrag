import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium

# Загрузка данных
data = pd.read_csv('kurty_river_data.csv')

# Обработка данных
data['date'] = pd.to_datetime(data['date'])
data['month'] = data['date'].dt.month
data['season'] = pd.cut(data['date'].dt.month, bins=[1, 3, 6, 9, 12], labels=['зима', 'весна', 'лето', 'осень'])

# Разделение данных на обучающую и тестовую выборки
X = data[['month', 'season']]
y = data['water_level']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Предсказание уровня воды в реке Курты
y_pred = model.predict(X_test)

# Оценка точности модели
print('Точность модели:', accuracy_score(y_test, y_pred))
print('Отчет о классификации:')
print(classification_report(y_test, y_pred))

# Создание карты с прогнозом уровня воды в реке Курты
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=10)
folium.Marker([data['latitude'].mean(), data['longitude'].mean()], popup='Прогноз уровня воды').add_to(m)

# Прогнозирование уровня воды в реке Курты на основе исторических трендов
future_data = pd.DataFrame({'month': [1, 2, 3], 'season': ['зима', 'весна', 'лето']})
future_pred = model.predict(future_data)
for i in range(len(future_pred)):
    folium.Marker([data['latitude'].mean(), data['longitude'].mean()], popup=f'Прогноз уровня воды на {future_data["month"][i]} месяц: {future_pred[i]}').add_to(m)

# Сохранение карты
m.save("57.html")