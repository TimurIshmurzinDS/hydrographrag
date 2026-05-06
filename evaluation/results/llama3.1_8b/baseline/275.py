import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from folium import Map, Marker
import matplotlib.pyplot as plt

# Загрузка данных
df = pd.read_csv('solar_cycles.csv')

# Обработка данных
X = df.drop(['солнечная вспышка'], axis=1)  # признаки
y = df['солнечная вспышка']  # целевая переменная

# Разделение данных на обучающую и проверочную выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка точности модели
accuracy = model.score(X_test, y_test)
print(f'Точность модели: {accuracy:.2f}')

# Предсказание вероятностей для новых данных
new_data = pd.DataFrame({'параметр1': [1.2], 'параметр2': [3.4]})  # пример новых данных
predictions = model.predict_proba(new_data)

# Визуализация результатов на карте
m = Map(location=[0, 0], zoom_start=2)
for i in range(len(predictions)):
    marker = Marker(location=[new_data.iloc[i]['параметр1'], new_data.iloc[i]['параметр2']], popup=f'Вероятность солнечной вспышки: {predictions[i][1]:.2f}')
    m.add_child(marker)

m.save("275.html")