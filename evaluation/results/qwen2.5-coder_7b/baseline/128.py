import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium

# Загрузка данных (пример)
data = {
    'Lepsy_Max_Level': [10, 12, 15, 18, 20, 22, 25, 27, 30, 32],
    'Dos_Max_Level': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
}
df = pd.DataFrame(data)

# Разделение данных на признаки и целевую переменную
X = df[['Lepsy_Max_Level']]
y = (df['Dos_Max_Level'] > 15).astype(int)  # Предполагаем, что паводок начинается, когда уровень воды в Dos River превышает 15

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание модели случайного леса
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Прогнозирование на тестовой выборке
y_pred = model.predict(X_test)

# Оценка качества модели
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Визуализация результатов на карте (пример)
m = folium.Map(location=[50.1234, 8.7654], zoom_start=10)

folium.Marker([50.1234, 8.7654], popup='Lepsy River').add_to(m)
folium.Marker([50.1235, 8.7655], popup='Dos River').add_to(m)

# Сохранение карты
m.save("128.html")