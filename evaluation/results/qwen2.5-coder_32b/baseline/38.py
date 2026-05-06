import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import folium

# Шаг 1: Сбор данных (примерные данные)
data = {
    'Загрязнение_промышленное': [0.2, 0.3, 0.4, 0.5, 0.6],
    'Загрязнение_сельское': [0.1, 0.2, 0.3, 0.4, 0.5],
    'Загрязнение_городское': [0.1, 0.2, 0.3, 0.4, 0.5],
    'Геологическая_характеристика': [0.2, 0.3, 0.4, 0.5, 0.6],
    'Гидрологическая_характеристика': [0.1, 0.2, 0.3, 0.4, 0.5],
    'Риск': [0, 0, 1, 1, 1]  # 0 - низкий риск, 1 - высокий риск
}

df = pd.DataFrame(data)

# Шаг 2: Подготовка данных
X = df.drop('Риск', axis=1)
y = df['Риск']

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Шаг 3: Выбор модели (Random Forest)
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Шаг 4: Обучение модели
model.fit(X_train, y_train)

# Шаг 5: Валидация модели
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Пример новых данных для оценки риска (координаты реки Каркара)
new_data = pd.DataFrame({
    'Загрязнение_промышленное': [0.3],
    'Загрязнение_сельское': [0.2],
    'Загрязнение_городское': [0.2],
    'Геологическая_характеристика': [0.4],
    'Гидрологическая_характеристика': [0.3]
})

# Шаг 6: Оценка риска
risk_level = model.predict(new_data)
print("Уровень экологического риска:", "Высокий" if risk_level[0] == 1 else "Низкий")

# Шаг 7: Визуализация результатов на карте (примерные координаты реки Каркара)
m = folium.Map(location=[43.25, 46.98], zoom_start=10)

# Добавление маркера с уровнем риска
folium.Marker(
    location=[43.25, 46.98],
    popup=f"Уровень экологического риска: {'Высокий' if risk_level[0] == 1 else 'Низкий'}",
    icon=folium.Icon(color='red' if risk_level[0] == 1 else 'green')
).add_to(m)

# Сохранение карты
m.save("38.html")